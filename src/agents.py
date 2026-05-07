from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .config import settings
from .tools import TOOLS


llm = ChatOpenAI(model=settings.model, api_key=settings.openai_api_key)


async def planner_agent(goal: str) -> str:
    messages = [
        SystemMessage(content="You are a planning agent. Break the goal into clear steps."),
        HumanMessage(content=goal),
    ]
    resp = await llm.ainvoke(messages)
    return resp.content


async def researcher_agent(task: str) -> str:
    # simple example: call search tool
    result = await TOOLS["search_web"](task)
    return f"Research for '{task}': {result}"


async def executor_agent(task: str, context: str) -> str:
    messages = [
        SystemMessage(content="You are an execution agent. Use the context to complete the task."),
        HumanMessage(content=f"Task: {task}\nContext:\n{context}"),
    ]
    resp = await llm.ainvoke(messages)
    return resp.content
