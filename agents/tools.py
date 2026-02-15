"""Custom tools available to the research assistant agents."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from agents.config import get_llm


@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information using the Tavily API.

    Parameters
    ----------
    query:
        The search query string.

    Returns
    -------
    str
        Formatted search results with titles, URLs, and content snippets.
    """
    # Lazy import so the dependency is only required at runtime when the tool
    # is actually invoked (Tavily is provided by langchain-community).
    from langchain_community.tools.tavily_search import TavilySearchResults

    search = TavilySearchResults(max_results=5)
    results = search.invoke(query)

    if not results:
        return "No results found."

    formatted: list[str] = []
    for idx, result in enumerate(results, 1):
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        content = result.get("content", "")
        formatted.append(f"[{idx}] {title}\n    {url}\n    {content}")

    return "\n\n".join(formatted)


@tool
def summarize(text: str) -> str:
    """Produce a concise summary of the provided text using the configured LLM.

    Parameters
    ----------
    text:
        The text to summarise.

    Returns
    -------
    str
        A concise summary.
    """
    llm = get_llm(temperature=0.0)
    messages = [
        SystemMessage(
            content=(
                "You are a concise summariser. Distil the following text into "
                "its key points using no more than five bullet points."
            )
        ),
        HumanMessage(content=text),
    ]
    response = llm.invoke(messages)
    return response.content
