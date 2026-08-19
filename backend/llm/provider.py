import requests
from backend.config import settings

class LLMProvider:
    def generate(self, messages, system=None):
        if not settings.llm_api_key:
            raise RuntimeError("LLM_API_KEY is not configured.")

        payload_messages = []
        if system:
            payload_messages.append({
                "role": "user",
                "content": "SYSTEM INSTRUCTIONS:\n" + system
            })
        payload_messages.extend(messages)

        response = requests.post(
            settings.llm_base_url,
            headers={
                "Authorization": f"Bearer {settings.llm_api_key}",
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.llm_model,
                "max_tokens": 1200,
                "messages": payload_messages,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        content = data.get("content")
        if isinstance(content, list):
            return "\n".join(
                x.get("text", "") for x in content
                if isinstance(x, dict) and x.get("text")
            ).strip()
        if isinstance(content, str):
            return content
        if isinstance(data.get("output_text"), str):
            return data["output_text"]

        raise RuntimeError("Unsupported LLM response shape.")

llm = LLMProvider()
