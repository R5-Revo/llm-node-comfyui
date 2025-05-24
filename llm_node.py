OPENAI_MODELS = [
    "gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"
]
ANTHROPIC_MODELS = [
    "claude-opus-4-20250514",
    "claude-sonnet-4-20250514",
    "claude-3-7-sonnet-20250219",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]
GOOGLE_MODELS = [
    "gemini-pro", "gemini-pro-vision"
]
GROQ_MODELS = [
    "llama2-70b-4096", "mixtral-8x7b-32768"
]
MISTRAL_MODELS = [
    "mistral-tiny", "mistral-small", "mistral-medium"
]

ALL_MODELS = (
    OPENAI_MODELS +
    ANTHROPIC_MODELS +
    GOOGLE_MODELS +
    GROQ_MODELS +
    MISTRAL_MODELS
)

PROVIDER_MODELS = {
    "openai": OPENAI_MODELS,
    "anthropic": ANTHROPIC_MODELS,
    "google": GOOGLE_MODELS,
    "groq": GROQ_MODELS,
    "mistral": MISTRAL_MODELS
}

class UniversalLLMNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": (list(PROVIDER_MODELS.keys()),),
                "model": (ALL_MODELS,),
                "api_key": ("STRING", {"multiline": False, "password": True}),  # 追加
                "prompt": ("STRING", {"multiline": True}),
                "max_tokens": ("INT", {"default": 300, "min": 50, "max": 4096}),
            }
        }
        
    RETURN_TYPES = ("STRING",)
    FUNCTION = "query"
    CATEGORY = "LLM/Universal"

    def query(self, provider, model, api_key, prompt, max_tokens):
        try:
            sdxl_prompt = (
                "You are a professional prompt engineer for Stable Diffusion XL (SDXL).\n"
                "Given a scene description or list of tags, convert them into a clean, high-quality positive prompt in SDXL format.\n"
                "Output the prompt as a single comma-separated line, with no explanations, no preface, and no extra text.\n"
                "Follow this tag order strictly: girl, hairstyle, hair color, bangs, eye color, facial expression, body type, breast size, pose, situation.\n"
                "Example: 1girl, long hair, blonde, straight bangs, blue eyes, smiling, slender, large breasts, sitting, by the lake in early summer\n"
                "Only output the prompt line.\n"
                f"Input: {prompt}"
            )

            if provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": sdxl_prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message.content,)

            elif provider == "anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                completion = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": sdxl_prompt}]
                )
                return (completion.content[0].text,)

            elif provider == "google":
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model_obj = genai.GenerativeModel(model)
                response = model_obj.generate_content(sdxl_prompt)
                return (response.text,)

            elif provider == "groq":
                from openai import OpenAI
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": sdxl_prompt}],
                    max_tokens=max_tokens,
                )
                return (completion.choices[0].message.content,)

            elif provider == "mistral":
                from openai import OpenAI
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.mistral.ai/v1"
                )
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": sdxl_prompt}],
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