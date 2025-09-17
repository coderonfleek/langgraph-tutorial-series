from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# --- 1. Define the Graph State ---
class GraphState(TypedDict):
    """Represents the state of our graph."""
    # The initial input provided to the graph.
    input: str
    # A list to trace the execution path.
    execution_path: list[str]

# --- 2. Define the Nodes ---
# A simple node that appends to the execution path.
def node_a(state: GraphState) -> dict:
    print("Executing Node A...")
    new_path = state.get("execution_path", []) + ["node_a"]
    return {"execution_path": new_path}

# Another simple node.
def node_b(state: GraphState) -> dict:
    print("Executing Node B...")
    new_path = state.get("execution_path", []) + ["node_b"]
    return {"execution_path": new_path}

def node_c(state: GraphState) -> dict:
    """A node in the 'conditional' path."""
    print("Executing Node C...")
    new_path = state.get("execution_path", []) + ["node_c"]
    return {"execution_path": new_path}

def node_d(state: GraphState) -> dict:
    """Another node in the 'conditional' path."""
    print("Executing Node D...")
    new_path = state.get("execution_path", []) + ["node_d"]
    return {"execution_path": new_path}

# --- 3. Define the Conditional Edge Function ---
# This function determines whether to go to C or D from B

def should_continue(state: GraphState) -> str:
    """A conditional edge function that routes the graph."""
    print("Evaluating conditional edge...")
    # Get the input to determine the next step.
    if "go_to_c" in state["input"]:
        print("-> Condition met: Routing to Node C.")
        # The return value must match a key in the conditional edge map.
        return "continue_c"
    else:
        print("-> Condition not met: Routing to Node D.")
        return "continue_d"
    
# --- 4. Build and Compile the Graph ---

builder = StateGraph(GraphState)

# Add all nodes
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)
builder.add_node("node_d", node_d)

# Normal Edge: From START to the first node.
builder.add_edge(START, "node_a")

# Normal Edge: From 'node_a' directly to 'node_b'.
builder.add_edge("node_a", "node_b")

# Conditional Edge: From 'node_b' to a conditional function that decides the next step.
builder.add_conditional_edges(
    "node_b",          # From node "node_b"...
    should_continue,   # ...use this function to decide the next node...
    {                  # ...with these specific mappings.
        "continue_c": "node_c",
        "continue_d": "node_d"
    }
)

# Normal Edges to terminate the graph.
builder.add_edge("node_c", END)
builder.add_edge("node_d", END)

graph = builder.compile()

# First invocation: The input does NOT contain 'go_to_c', so the path is A -> B -> D.
initial_state_1 = {"input": "Hello, this is a message."}
final_state_1 = graph.invoke(initial_state_1)
print("\nFinal State (Path A->B->D):", final_state_1)

print("\n" + "="*50 + "\n")

print("--- Example 2: Path is A -> B -> C ---")

# Second invocation: The input DOES contain 'go_to_c', so the path is A ->B -> C.
initial_state_2 = {"input": "Hello, go_to_c to continue."}
final_state_2 = graph.invoke(initial_state_2)
print("\nFinal State (Path A->B->C):", final_state_2)