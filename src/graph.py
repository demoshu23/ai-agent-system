from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .memory import memory
from .agents import planner_agent, researcher_agent, executor_agent


# State schema for LangGraph
class AgentState(Dict[str, Any]):
    pass


async def node_plan(state: AgentState) -> AgentState:
    plan = await planner_agent(state["goal"])
    return {**state, "plan": plan}


async def node_research(state: AgentState) -> AgentState:
    research = await researcher_agent(state["plan"])
    return {**state, "research": research}


async def node_execute(state: AgentState) -> AgentState:
    result = await executor_agent(state["plan"], state["research"])
    return {**state, "result": result}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("plan", node_plan)
    graph.add_node("research", node_research)
    graph.add_node("execute", node_execute)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "research")
    graph.add_edge("research", "execute")
    graph.add_edge("execute", END)

    # LangGraph checkpointing (in‑memory) – you can swap with Redis/Postgres
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


graph_app = build_graph()


async def run_workflow(session_id: str, goal: str) -> AgentState:
    # load previous state if needed
    state = memory.load(session_id)
    state.update({"goal": goal})

    final_state = None
    async for s in graph_app.astream(state, config={"configurable": {"thread_id": session_id}}):
        final_state = s

    memory.save(session_id, final_state)
    return final_state
