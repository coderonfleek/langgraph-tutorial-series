"""
Experimenting with different methods for creating Agent Graph state
"""
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from dataclasses import dataclass
from pydantic import Field, BaseModel
from langchain_core.messages import BaseMessage

"""
[ Initial/Startup Code ]
"""
"""
State variables
    - messages: A list of messages
    - step_count: A counter to be incremented with each node hop
    - private_data: Some random string data
"""

# Start with a function that takes a graph state created using any of the methods and also the initialization state

# Nodes

def node_a(state):
    """A simple node that updates the state."""
    print("Executing Node A...")
    return {
        "messages": ["Step A Completed"],
        "step_count": 1
    }

def node_b(state):
    """A simple node that updates the state."""
    print("Executing Node B...")
    # Access and print some state information for demonstration
    if isinstance(state, dict):
        step_count = state["step_count"]
    else:
        step_count = state.step_count
    
    print(f"Current step count from state: {step_count}")

    return {
        "messages": ["Step B Completed"],
        "step_count": 1
    }

def build_and_run_graph(state_schema, initial_state):
    print(f"\n--- Building and Running graph with state schema: {state_schema.__name__ if hasattr(state_schema, '__name__') else 'Dictionary'}")

    # Initiate the Graph
    graph = StateGraph(state_schema)

    # Add Nodes
    graph.add_node("node_a", node_a)
    graph.add_node("node_b", node_b)

    # Add Edges
    graph.add_edge(START, "node_a")
    graph.add_edge("node_a", "node_b")
    graph.add_edge("node_b", END)

    agent = graph.compile()

    final_state = agent.invoke(initial_state)

    print("\nFinal State:")
    print(final_state)
    print("-"* 40)


# [ Demo Code Starts here ]

"""
--- METHOD 1: Using a simple Dictionary ---
- Most basic implementation, requires no dependencies
- Lacks type safety and can be hard to manage in complex applications
- Can only the default reducer
"""

def create_dict_state():
    return {
        "messages": [],
        "step_count": 0,
        "private_data": None
    }


build_and_run_graph(dict, create_dict_state()) 


"""
--- METHOD 2: Using a TypedDict ---
- Common and simple way to add type hints
- Works seamlessly with LangGraph
- Provides a schema but does not allow for default values or validation
"""


# Create a custom reducer for step_count
def custom_add(current: int, new: int):
    #A custom reducer to step_count with the new value
    return current + new


class TypedDictState(TypedDict):
    messages: Annotated[List[str], add_messages]
    step_count: Annotated[int, custom_add]
    private_data: str

# Build and run the graph with the TypedDict state 
""" 
build_and_run_graph(TypedDictState, {
    "messages": [],
    "step_count": 0,
    "private_data": ""
})  
"""


"""
--- METHOD 3: Using a Dataclass ---
- Great choice for providing default values along with type hints
- More verbose than TypeDict
- Default values help handle initialization
"""
""" @dataclass
class DataClassState:
    messages: Annotated[List[str], add_messages]
    step_count: Annotated[int, custom_add]
    private_data: str = ""

# Create state using dataclass and provide defaults
build_and_run_graph(DataClassState, DataClassState(
    messages = [],
    step_count = 0
)) """

"""
--- METHOD 4: Using a Pydantic Model with Fields ---
- Pydantic is a powerful library for data validation and schema definition.
- Using Field() allows for more granular control, including providing default factories for mutable types like lists.
"""
class PydanticState(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)
    step_count : Annotated[int, custom_add] = Field(default=0)
    private_data: str = Field(default="")

"""
build_and_run_graph(PydanticState, PydanticState())
"""
