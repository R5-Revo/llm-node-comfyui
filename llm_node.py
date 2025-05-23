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
                import openai
                openai.api_key = os.getenv("OPENAI_API_KEY")
                completion = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message["content"],)

            elif provider == "anthropic":
                import anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                client = anthropic.Anthropic(api_key=api_key)
                completion = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return (completion.content[0].text,)

            elif provider == "google":
                import google.generativeai as genai
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model_obj = genai.GenerativeModel(model)
                response = model_obj.generate_content(prompt)
                return (response.text,)

            elif provider == "groq":
                import openai
                openai.api_key = os.getenv("GROQ_API_KEY")
                openai.api_base = "https://api.groq.com/openai/v1"
                completion = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message["content"],)

            elif provider == "mistral":
                import openai
                openai.api_key = os.getenv("MISTRAL_API_KEY")
                openai.api_base = "https://api.mistral.ai/v1"
                completion = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message["content"],)

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
