import httpx
from typing import Any, Dict


async def search_web(query: str) -> str:
    # placeholder – swap with real search API
    async with httpx.AsyncClient(timeout=10) as client:
        # call your internal search / RAG API here
        return f"Search results for: {query}"


def calculate(a: float, b: float, op: str = "+") -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b
    raise ValueError("Unsupported op")


TOOLS: Dict[str, Any] = {
    "search_web": search_web,
    "calculate": calculate,
}
