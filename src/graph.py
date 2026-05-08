from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .agents import planner_agent, researcher_agent, executor_agent


class AgentState(Dict[str, Any]):
    pass


async def node_plan(state: AgentState) -> AgentState:
    goal = state["goal"]
    plan = await planner_agent(goal)
    return {"plan": plan}


async def node_research(state: AgentState) -> AgentState:
    plan = state["plan"]
    research = await researcher_agent(plan)
    return {"research": research}


async def node_execute(state: AgentState) -> AgentState:
    plan = state["plan"]
    research = state["research"]
    result = await executor_agent(plan, research)
    return {"result": result}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("plan", node_plan)
    graph.add_node("research", node_research)
    graph.add_node("execute", node_execute)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "research")
    graph.add_edge("research", "execute")
    graph.add_edge("execute", END)

    return graph.compile()

    # checkpointer = MemorySaver()
    # return graph.compile(checkpointer=checkpointer)


graph_app = build_graph()


async def run_workflow(session_id: str, goal: str) -> AgentState:
    state: AgentState = {
        "goal": goal,
    }

    final_state = None
    async for s in graph_app.astream(
        state,
        config={"configurable": {"thread_id": session_id}},
    ):
        final_state = s

    return final_state or state
