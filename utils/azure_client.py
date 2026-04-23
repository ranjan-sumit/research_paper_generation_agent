"""
Azure OpenAI client wrapper supporting text and vision calls.
"""
import base64
from openai import AzureOpenAI


class AzureOpenAIClient:
    def __init__(self, endpoint: str, api_key: str, deployment: str, api_version: str = "2024-02-01"):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        self.deployment = deployment

    def chat(self, system: str, user: str, temperature: float = 0.3, max_tokens: int = 4000) -> str:
        """Simple text chat completion."""
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

    def chat_json(self, system: str, user: str, max_tokens: int = 4000) -> str:
        """Chat completion that instructs model to return JSON."""
        system_with_json = system + "\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown, no code fences, no explanation."
        return self.chat(system_with_json, user, temperature=0.1, max_tokens=max_tokens)

    def vision(self, system: str, user_text: str, image_bytes: bytes, max_tokens: int = 1500) -> str:
        """Vision call — send an image alongside text."""
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                    ],
                },
            ],
            temperature=0.1,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
