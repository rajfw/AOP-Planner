import asyncio
import json
import logging
import uuid
import sys
from dependencies import get_llm_client

# Mock everything by directly interacting with the graph if the API isn't running, 
# OR test the graph directly. API testing is better for integration.
# But since I cannot easily start the server and keep it running while I run another script 
# (unless I use background process), testing the graph logic directly is safer for this environment.

from workflows.prd_agent import app_graph

async def test_workflow():
    print("Starting Workflow Test...")
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # 1. Start Workflow
    initial_state = {
        "prd_content": "This is a weak PRD. It needs better metrics.",
        "improvement_type": "comprehensive",
        "messages": []
    }
    
    print(f"1. Invoking Graph (Thread: {thread_id})...")
    # This should stop at human_review
    await app_graph.ainvoke(initial_state, config=config)
    
    state = await app_graph.aget_state(config)
    print(f"2. Current Node: {state.next}")
    if "human_review" in state.next:
        print("SUCCESS: Graph paused at human_review.")
    else:
        print(f"FAILURE: Graph did not pause where expected. Next: {state.next}")
        return

    # 3. Simulate Feedback (Rejection/Improvement)
    print("3. Sending Feedback (Requesting more changes)...")
    await app_graph.aupdate_state(config, {"feedback": "Make it shorter."}, as_node="human_review")
    
    # Resume - should go back to 'generate' because of feedback
    print("4. Resuming Graph...")
    await app_graph.ainvoke(None, config=config)
    
    state = await app_graph.aget_state(config)
    print(f"5. Current Node after feedback: {state.next}")
    # It should have run generate -> human_review (pause) again
    if "human_review" in state.next:
        print("SUCCESS: Graph returned to human_review after feedback.")
    else:
         print(f"FAILURE: Graph behavior unexpected. Next: {state.next}")

    # 6. Simulate Approval
    print("6. Sending Approval...")
    # Update state to clear feedback or set flag? In my logic route_after_review checks for 'feedback'.
    # If I don't clear 'feedback', it might loop forever.
    # The 'generate' node appends feedback to prompt, but doesn't clear it from state unless we do it.
    # We should probably clear feedback in the generate node or here.
    # Let's clear it here to simulate "fresh approval".
    await app_graph.aupdate_state(config, {"feedback": None}, as_node="human_review")
    
    await app_graph.ainvoke(None, config=config)
    
    state = await app_graph.aget_state(config)
    print(f"7. Final State Next: {state.next}")
    if not state.next: #(Empty tuple means END)
        print("SUCCESS: Graph completed to END.")
        print(f"Final Output: {state.values.get('improved_content')[:50]}...")
    else:
        print("FAILURE: Graph did not finish.")

if __name__ == "__main__":
    asyncio.run(test_workflow())
