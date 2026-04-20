class PromptPrefixNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"default": "", "multiline": True}),
                "prefix": ("STRING", {"default": "", "multiline": True}),
                "enabled": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "Holly/Prompting"

    def build_prompt(self, user_prompt, prefix, enabled):
        if not enabled:
            return ((user_prompt or "").strip(),)
        if not (prefix or "").strip():
            return ((user_prompt or "").strip(),)
        return (f"{prefix.strip()}\n{(user_prompt or '').strip()}".strip(),)


class PromptWithImageTagsNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "user_prompt": ("STRING", {"default": "", "multiline": True}),
                "prefix": ("STRING", {"default": "", "multiline": True}),
                "image_tags": ("STRING", {"default": "", "multiline": True}),
                "enabled": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "Holly/Prompting"

    def build_prompt(self, image, user_prompt, prefix, image_tags, enabled):
        _ = image  # Presence in graph is intentional; data is not transformed in this node.
        if not enabled:
            return ((user_prompt or "").strip(),)

        parts = []
        if (prefix or "").strip():
            parts.append(prefix.strip())
        if (image_tags or "").strip():
            parts.append(image_tags.strip())
        if (user_prompt or "").strip():
            parts.append(user_prompt.strip())

        return ("\n".join(parts).strip(),)
