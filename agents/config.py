"""LLM provider configuration with multi-provider support."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

load_dotenv()

_DEFAULTS: dict[str, dict[str, str]] = {
    "openai": {"model": "gpt-4o", "env_key": "OPENAI_API_KEY"},
    "anthropic": {"model": "claude-sonnet-4-5-20250929", "env_key": "ANTHROPIC_API_KEY"},
}


def get_llm(
    *,
    provider: str | None = None,
    model: str | None = None,
    temperature: float = 0.0,
):
    """Return a chat model instance based on the configured provider.

    Resolution order for *provider*:
        1. Explicit ``provider`` argument.
        2. ``LLM_PROVIDER`` environment variable.
        3. Falls back to ``"openai"``.

    Parameters
    ----------
    provider:
        ``"openai"`` or ``"anthropic"``.
    model:
        Override the default model name for the chosen provider.
    temperature:
        Sampling temperature. Defaults to ``0.0`` for deterministic output.

    Returns
    -------
    ChatOpenAI | ChatAnthropic
        A ready-to-use chat model.

    Raises
    ------
    ValueError
        If the provider string is not recognised.
    RuntimeError
        If the required API key environment variable is not set.
    """
    provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower().strip()

    if provider not in _DEFAULTS:
        raise ValueError(
            f"Unknown LLM provider '{provider}'. Choose from: {', '.join(_DEFAULTS)}"
        )

    cfg = _DEFAULTS[provider]
    model = model or cfg["model"]

    api_key = os.getenv(cfg["env_key"])
    if not api_key:
        raise RuntimeError(
            f"{cfg['env_key']} environment variable is required for provider '{provider}'"
        )

    if provider == "openai":
        return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)

    return ChatAnthropic(model=model, temperature=temperature, api_key=api_key)
