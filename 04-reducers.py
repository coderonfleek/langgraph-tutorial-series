from langgraph.graph import StateGraph, END, START
from typing import TypedDict, Annotated, List
from operator import add
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages

def run_example(name: str, state_schema: type, node_func: callable, initial_state: dict):
    """
    Builds and runs a simple graph with a given state schema, node, and initial state.
    """
    print(f"--- Running Example: {name} ---")
    graph = StateGraph(state_schema)
    graph.add_node("update_node", node_func)
    graph.add_edge(START, "update_node")
    graph.add_edge("update_node", END)

    app = graph.compile()

    final_state = app.invoke(initial_state)

    print(f"Initial State: {initial_state}")
    print(f"Final State: {final_state}")
    print("-" * 40)


# Example 1: State without a Reducer
class StateWithoutReducer(TypedDict):
    count: int
    animals: List[str]

# Example 2: State with custom reducer
def custom_increment(current: int, new: int) -> int:
    # A custom reducer that adds the new value to the current value.
    
    return current + new

class StateWithCustomReducer(TypedDict):
    count: Annotated[int, custom_increment]
    animals: Annotated[List[str], add]

# Example - State with Messages
class StateWithMessages(TypedDict):
    messages: Annotated[List[HumanMessage], add_messages]

def node_messages_reducer(state: StateWithMessages) -> dict:
    return {"messages": [HumanMessage(content="Hello from the node!")]}

""" Running the Graph """
def node_to_update(state: StateWithCustomReducer) -> dict:
    print(f"Node: Current state is {state}")
    #This will completly replace the state
    return {
        "count": 1,
        "animals": ["cat"]
    }

start_state = {
    "count": 5,
    "animals": ["lion", "tiger"]
}

# Run Example with no reducer
""" 
run_example(
    name="No Reducer",
    state_schema=StateWithoutReducer,
    node_func=node_to_update,
    initial_state=start_state
) 
"""

# Run with Custom reducer
""" 
run_example(
    name="Using a Custom Reducer",
    state_schema=StateWithCustomReducer,
    node_func=node_to_update,
    initial_state=start_state
) 
"""

# Run Messages example
run_example(
    name="`add_messages` Reducer",
    state_schema=StateWithMessages,
    node_func=node_messages_reducer,
    initial_state={"messages": [HumanMessage(content="Initial message.")]}
)
