# app/services/llm_client.py
import logging
from typing import Any

from ..core.config import settings
from ..utils.errors import LLMServiceError

logger = logging.getLogger("app.services.llm_client")


class LLMClient:
    """
    Service class responsible for talking to the actual LLM API.
    Replace the `simulate_llm_call` with a real HTTP call or SDK usage.
    """

    def __init__(self):
        self.base_url = settings.LLM_API_BASE_URL
        self.api_key = settings.LLM_API_KEY

    async def ask(self, prompt: str, max_tokens: int | None = 256) -> dict[str, Any]:
        try:
            logger.debug("Sending prompt to LLM", extra={"prompt_preview": prompt[:50]})

            # TODO: replace this with a real HTTP/SDK call to the model provider
            # For example:
            #   async with httpx.AsyncClient() as client:
            #       response = await client.post(...)
            #       response.raise_for_status()
            #       data = response.json()

            data = await self._simulate_llm_call(prompt, max_tokens)

            logger.debug("Received response from LLM", extra={"raw_response": data})

            return data

        except Exception as e:
            logger.exception("Error while calling LLM service")
            # Wrap and raise as our domain-specific error
            raise LLMServiceError("Failed to get response from LLM") from e

    async def _simulate_llm_call(
        self, prompt: str, max_tokens: int | None
    ) -> dict[str, Any]:
        """
        Simulate LLM behavior. In real scenario, this is replaced by actual API call.
        """
        # Simple "dummy" answer
        answer = f"Echo from LLM: {prompt[:200]}"
        return {
            "answer": answer,
            "model": "dummy-llm-001",
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": min(max_tokens or 0, 50),
            },
        }
