import logging
import operator
from typing import TypedDict, Annotated, List, Union, Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver

from dependencies import get_llm_client

logger = logging.getLogger("aop_planner.workflow")

# Define State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    prd_content: str
    improvement_type: str
    improved_content: str
    feedback: Optional[str]

# Nodes
def analyze_prd(state: AgentState):
    """Initial analysis (optional step, just logging for now)."""
    logger.info(f"Analyzing PRD of length {len(state['prd_content'])}")
    return {"messages": [SystemMessage(content="PRD Analysis complete.")]}

def generate_improvement(state: AgentState):
    """Call LLM to improve PRD."""
    # We use the raw client wrapper or langchain wrapper. Let's use direct client or langchain wrapper. 
    # Since we added langchain-openai to requirements, we can use it.
    
    # We need to access the client configuration. 
    # Ideally, we inject this, but for simplicity in this module:
    import os
    api_key = os.getenv("OPENAI_API_KEY", "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7Im5hbWUiOiJSYWplc3dhciBQIFMiLCJlbWFpbCI6InJhamVzd2FyLnN1YnJhbWFuaUBmcmVzaHdvcmtzLmNvbSIsImltYWdlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0FBUkNWSktyMjhxbU0xRTdnUE1fSlhPcDU4MEZHM2prNThMYzQ1SVB6eVFqN0lxWF89czk2LWMifSwianRpIjoiUGNVU0xxOFNrR3lYdmF1aFlEQTdsIiwiaWF0IjoxNzcwNzg2NTYwLCJleHAiOjE3NzEzOTEzNjB9.JglVKNUeldw7thE2swT0jiXKkf2M3DNUCZZ0WAIAWOg")
    base_url = os.getenv("OPENAI_BASE_URL", "https://cloudverse.freshworkscorp.com/api/v1")
    
    llm = ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model="Azure-GPT-5-chat",
        temperature=0.7
    )
    
    prompt_templates = {
        "comprehensive": "As a product expert, improve this PRD provided below. Focus on clarity, completeness, and success metrics.",
        "clarify": "Simplify and clarify the language of this PRD.",
        "expand": "Expand the details of this PRD, adding user stories and edge cases."
    }
    
    system_prompt = prompt_templates.get(state["improvement_type"], prompt_templates["comprehensive"])
    
    # Check for feedback from HITL loop
    if state.get("feedback"):
        system_prompt += f"\n\nAdditional User Feedback to incorporate: {state['feedback']}"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["prd_content"])
    ]
    
    response = llm.invoke(messages)
    return {"improved_content": response.content}

# In-memory checkpointer for HITL state persistence
checkpointer = MemorySaver()

# Graph Construction
workflow = StateGraph(AgentState)

workflow.add_node("analyze", analyze_prd)
workflow.add_node("generate", generate_improvement)
def human_review(state: AgentState):
    pass 

workflow.add_node("human_review", human_review)

workflow.set_entry_point("analyze")
workflow.add_edge("analyze", "generate")
workflow.add_edge("generate", "human_review")

def route_after_review(state: AgentState):
    if state.get("feedback"):
        return "generate"
    return END

workflow.add_conditional_edges(
    "human_review",
    route_after_review,
    {
        "generate": "generate",
        END: END
    }
)

app_graph = workflow.compile(checkpointer=checkpointer, interrupt_before=["human_review"])
