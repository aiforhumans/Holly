import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_FILE_NAME = "holly_prompt.db"


def _now():
    return datetime.now(timezone.utc).isoformat()


def _ensure_schema(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prompt_history (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            user_id TEXT NOT NULL,
            raw_prompt TEXT NOT NULL,
            final_prompt TEXT NOT NULL,
            target_model TEXT NOT NULL,
            strategy_mode TEXT NOT NULL,
            score INTEGER NOT NULL,
            liked INTEGER NOT NULL,
            notes TEXT NOT NULL,
            intent_map_json TEXT NOT NULL,
            strategy_profile_json TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id TEXT PRIMARY KEY,
            profile_json TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def _db_path():
    env_path = os.environ.get("HOLLY_PROMPT_DB_PATH", "").strip()
    if env_path:
        return Path(env_path)
    return DATA_DIR / DB_FILE_NAME


def _connect():
    db_path = _db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    return conn


@contextmanager
def _connection():
    conn = _connect()
    try:
        yield conn
    finally:
        conn.close()


def _tokenize(text):
    return {w for w in (text or "").lower().split() if len(w) > 2}


def _recompute_profile(conn, user_id):
    rows = conn.execute(
        """
        SELECT score, liked, strategy_mode
        FROM prompt_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        """,
        (user_id,),
    ).fetchall()

    if not rows:
        profile = {
            "user_id": user_id,
            "prompt_count": 0,
            "avg_score": 0.0,
            "liked_ratio": 0.0,
            "preferred_mode": "enhance",
        }
    else:
        prompt_count = len(rows)
        avg_score = sum(r["score"] for r in rows) / max(prompt_count, 1)
        liked_ratio = sum(r["liked"] for r in rows) / max(prompt_count, 1)

        mode_counts = {}
        for row in rows:
            mode = row["strategy_mode"] or "enhance"
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        preferred_mode = sorted(mode_counts.items(), key=lambda x: x[1], reverse=True)[0][0]

        profile = {
            "user_id": user_id,
            "prompt_count": prompt_count,
            "avg_score": round(avg_score, 3),
            "liked_ratio": round(liked_ratio, 3),
            "preferred_mode": preferred_mode,
        }

    conn.execute(
        """
        INSERT INTO user_preferences(user_id, profile_json, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile_json = excluded.profile_json,
            updated_at = excluded.updated_at
        """,
        (user_id, json.dumps(profile, ensure_ascii=True), _now()),
    )
    conn.commit()
    return profile


def save_trace(record):
    trace_id = str(uuid.uuid4())
    user_id = (record.get("user_id") or "default").strip() or "default"
    intent_map_json = json.dumps(record.get("intent_map", {}), ensure_ascii=True)
    strategy_profile_json = json.dumps(record.get("strategy_profile", {}), ensure_ascii=True)
    strategy_mode = (record.get("strategy_profile", {}).get("mode") or "enhance").strip()

    with _connection() as conn:
        conn.execute(
            """
            INSERT INTO prompt_history(
                id, timestamp, user_id, raw_prompt, final_prompt, target_model,
                strategy_mode, score, liked, notes, intent_map_json, strategy_profile_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trace_id,
                _now(),
                user_id,
                record.get("raw_prompt", ""),
                record.get("final_prompt", ""),
                record.get("target_model", "z-image-turbo"),
                strategy_mode,
                int(record.get("score", 0)),
                int(bool(record.get("liked", False))),
                record.get("notes", ""),
                intent_map_json,
                strategy_profile_json,
            ),
        )
        conn.commit()
        profile = _recompute_profile(conn, user_id)

    return trace_id, profile


def get_trace(trace_id):
    with _connection() as conn:
        row = conn.execute(
            "SELECT * FROM prompt_history WHERE id = ?",
            (trace_id,),
        ).fetchone()
    if row is None:
        return {}

    return {
        "trace_id": row["id"],
        "timestamp": row["timestamp"],
        "user_id": row["user_id"],
        "raw_prompt": row["raw_prompt"],
        "final_prompt": row["final_prompt"],
        "target_model": row["target_model"],
        "strategy_mode": row["strategy_mode"],
        "score": row["score"],
        "liked": bool(row["liked"]),
        "notes": row["notes"],
        "intent_map": json.loads(row["intent_map_json"] or "{}"),
        "strategy_profile": json.loads(row["strategy_profile_json"] or "{}"),
    }


def retrieve_similar(raw_prompt, top_k=5, user_id=None):
    top_k = max(1, min(int(top_k), 20))
    query_tokens = _tokenize(raw_prompt)
    scoped_user = (user_id or "").strip()

    with _connection() as conn:
        if scoped_user:
            rows = conn.execute(
                """
                SELECT id, timestamp, raw_prompt, final_prompt, target_model, score, liked
                FROM prompt_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 300
                """,
                (scoped_user,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, timestamp, raw_prompt, final_prompt, target_model, score, liked
                FROM prompt_history
                ORDER BY timestamp DESC
                LIMIT 300
                """
            ).fetchall()

    ranked = []
    for row in rows:
        candidate_text = f"{row['raw_prompt']} {row['final_prompt']}"
        candidate_tokens = _tokenize(candidate_text)
        overlap = len(query_tokens.intersection(candidate_tokens))
        denom = max(1, len(query_tokens.union(candidate_tokens)))
        similarity = overlap / denom
        ranked.append(
            {
                "trace_id": row["id"],
                "timestamp": row["timestamp"],
                "raw_prompt": row["raw_prompt"],
                "final_prompt": row["final_prompt"],
                "target_model": row["target_model"],
                "score": row["score"],
                "liked": bool(row["liked"]),
                "similarity": round(similarity, 4),
            }
        )

    ranked.sort(key=lambda x: (x["similarity"], x["score"], x["timestamp"]), reverse=True)
    return ranked[:top_k]


def get_profile(user_id):
    uid = (user_id or "default").strip() or "default"
    with _connection() as conn:
        row = conn.execute(
            "SELECT profile_json FROM user_preferences WHERE user_id = ?",
            (uid,),
        ).fetchone()
        if row is not None:
            try:
                return json.loads(row["profile_json"])
            except Exception:
                pass
        return _recompute_profile(conn, uid)
