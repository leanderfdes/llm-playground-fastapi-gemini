# app/core/config.py
"""
Application configuration using pydantic-settings (Pydantic v2 style).

This file:
- Loads environment variables from a local .env when present (env_file configured).
- Exposes typed settings for the app and LLM clients.
- Provides convenient helpers for CORS origins parsing and safe defaults.

Important:
- Do NOT commit your real .env file to the repo. Use Render/Vercel environment variables
  for production secrets (GEMINI_API_KEY, OPENAI_API_KEY, etc.).
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App metadata
    APP_NAME: str = "LLM API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # LLM / provider config
    # The server-side Gemini API key (server only). Must be set in Render/Cloud Run.
    GEMINI_API_KEY: Optional[str] = None
    # Optional OpenAI key (if you support OpenAI fallback)
    OPENAI_API_KEY: Optional[str] = None

    # Base URL to reach an external LLM service if applicable (not required)
    LLM_API_BASE_URL: Optional[str] = None

    # Default model name to use for Gemini (can be overridden where you construct client)
    GEMINI_DEFAULT_MODEL: str = "models/gemini-2.5-flash"

    # A comma-separated list of allowed CORS origins. Example:
    # "https://your-frontend.vercel.app,http://localhost:5173"
    ALLOWED_ORIGINS: Optional[str] = None

    # Feature toggles / runtime options
    # If True, allow all origins (use only during testing; avoid in production)
    CORS_ALLOW_ALL: bool = False

    # Token limits enforced server-side (sensible defaults; clamp in service)
    DEFAULT_MAX_TOKENS: int = 1024
    MAX_ALLOWED_TOKENS: int = 100000
    MIN_ALLOWED_TOKENS: int = 1

    # Pydantic v2 style config: load .env automatically in development
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unknown env vars rather than error
    )

    # --- convenience helpers (not part of settings to set via env) ---

    def cors_origins(self) -> List[str]:
        """
        Return a parsed list of allowed CORS origins.

        Priority:
        - If CORS_ALLOW_ALL is True -> return ["*"]
        - If ALLOWED_ORIGINS is set -> split by comma and strip whitespace
        - Else return sensible local defaults for development (Vite)
        """
        if self.CORS_ALLOW_ALL:
            return ["*"]

        if self.ALLOWED_ORIGINS:
            # split by comma and remove empty items
            origins = [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]
            # Ensure local dev origins are present (helps local testing)
            defaults = ["http://localhost:5173", "http://127.0.0.1:5173"]
            # Merge keeping order and avoiding duplicates
            merged = []
            for o in origins + defaults:
                if o not in merged:
                    merged.append(o)
            return merged

        # fallback defaults for local development (no env set)
        return ["http://localhost:5173", "http://127.0.0.1:5173"]


# instantiate one settings object for import across the app
settings = Settings()
