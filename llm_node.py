import os

class UniversalLLMNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": (["openai", "anthropic", "google", "groq", "mistral"],),
                "model": ("STRING", {"default": "claude-3-sonnet-20240229"}),
                "prompt": ("STRING", {"multiline": True}),
                "max_tokens": ("INT", {"default": 300, "min": 50, "max": 4096}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "query"
    CATEGORY = "LLM/Universal"

    def query(self, provider, model, prompt, max_tokens):
        try:
            if provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message.content,)

            elif provider == "anthropic":
                import anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                client = anthropic.Anthropic(api_key=api_key)
                sdxl_prompt = (
                    "You are a professional prompt engineer for Stable Diffusion XL (SDXL).\n"
                    "Given a scene description or list of tags, convert them into a clean, high-quality positive prompt in SDXL format.\n"
                    "Output the prompt as a single comma-separated line, with no explanations, no preface, and no extra text.\n"
                    "Follow this tag order strictly: girl, hairstyle, hair color, bangs, eye color, facial expression, body type, breast size, pose, situation.\n"
                    "Example: 1girl, long hair, blonde, straight bangs, blue eyes, smiling, slender, large breasts, sitting, by the lake in early summer\n"
                    "Only output the prompt line.\n"
                    f"Input: {prompt}"
                )
                completion = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": sdxl_prompt}]
                )
                return (completion.content[0].text,)

            elif provider == "google":
                import google.generativeai as genai
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model_obj = genai.GenerativeModel(model)
                response = model_obj.generate_content(prompt)
                return (response.text,)

            elif provider == "groq":
                from openai import OpenAI
                client = OpenAI(
                    api_key=os.getenv("GROQ_API_KEY"),
                    base_url="https://api.groq.com/openai/v1"
                )
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message.content,)

            elif provider == "mistral":
                from openai import OpenAI
                client = OpenAI(
                    api_key=os.getenv("MISTRAL_API_KEY"),
                    base_url="https://api.mistral.ai/v1"
                )
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message.content,)

            else:
                return ("[ERROR] Unsupported provider.",)

        except Exception as e:
            return (f"[LLM Error] {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "UniversalLLMNode": UniversalLLMNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UniversalLLMNode": "Universal LLM Prompt"
}