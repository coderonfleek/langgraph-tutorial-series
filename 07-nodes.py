# This file demonstrates the creation of nodes in LangGraph,
# the arguments they can accept, and how they update the state.

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime


# --- 1. Define the Graph State ---
# This schema defines the shared data structure for our graph.
class GraphState(TypedDict):
    """Represents the state of our graph."""
    # The initial input provided to the graph.
    input: str
    # A variable to store the results from our nodes.
    results: str


# --- 2. Define a Runtime Context (Optional) ---
# We now define this as a separate schema for type-safety.
class ContextSchema(TypedDict):
    """Contains information available at runtime, not stored in the state."""
    user_id: str


# --- 3. Define the Nodes ---
# All nodes are standard Python functions.
# Each function represents a specific action in the workflow.

# Node A: A simple node that only takes the state as an argument.
def plain_node(state: GraphState) -> dict:
    """A node that simply updates the state's 'results' key."""
    print("Executing plain_node...")
    # This node returns a partial update to the state.
    return {"results": f"Hello, {state['input']}!"}


# Node B: Demonstrates how to access the RunnableConfig.
def node_with_config(state: GraphState, config: RunnableConfig) -> dict:
    """Accesses a value from the RunnableConfig."""
    print("Executing node_with_config...")
    thread_id = config.get("configurable", {}).get("thread_id")
    print(f"-> In node, accessed 'thread_id' from config: {thread_id}")
    # Updates the results with a new value.
    return {"results": "Config access successful."}


# Node C: Demonstrates how to access a custom Runtime context.
def node_with_runtime(state: GraphState, runtime: Runtime[ContextSchema]) -> dict:
    """Accesses a value from the custom runtime context."""
    print("Executing node_with_runtime...")
    # The runtime object has a .context property that holds our custom data.
    # We now access the user_id from the context attribute of the runtime object.
    user_id = runtime.context["user_id"]
    print(f"-> In node, accessed 'user_id' from runtime: {user_id}")
    # Updates the results with another new value.
    return {"results": "Runtime access successful."}


# --- 4. Build the Graph ---
def build_graph() -> StateGraph:
    """Builds and compiles the graph with all its nodes and edges."""
    # Create the graph builder with our defined state.
    # We now also provide the context_schema to the StateGraph constructor.
    builder = StateGraph(GraphState, context_schema=ContextSchema)

    # Add the nodes to the graph.
    # The name of the node is provided as the first argument.
    builder.add_node("plain_node", plain_node)
    builder.add_node("config_node", node_with_config)
    builder.add_node("runtime_node", node_with_runtime)

    # Define the sequential flow between nodes using edges.
    builder.add_edge(START, "plain_node")
    builder.add_edge("plain_node", "config_node")
    builder.add_edge("config_node", "runtime_node")
    builder.add_edge("runtime_node", END)

    # Compile the graph for execution.
    return builder.compile()


if __name__ == "__main__":
    app = build_graph()

    # Define the initial state for the graph.
    initial_state = {"input": "World"}
    
    # Define a custom RuntimeContext object.
    # runtime_context = ContextSchema(user_id="alice_smith")

    # Define a RunnableConfig with both a configurable value and the custom runtime.
    run_config = {
        "configurable": {
            "thread_id": "user-1234",
        }
    }

    print("--- Invoking the graph ---")
    final_state = app.invoke(
        input=initial_state,
        config=run_config,
        context={"user_id": "alice_smith"}
    )

    print("\n--- Final State of the Graph ---")
    print(final_state)
