from langgraph.graph import StateGraph, START, END

# We will also use 'typing' for better code clarity, though a simple
# dictionary would work just as well for the state.
from typing import TypedDict, Annotated

# The 'add_messages' function is a helper from LangGraph to easily manage a list.
from langgraph.graph.message import add_messages

# 1. Define the State
# We'll define a simple state that holds a list of messages.
class SimpleState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Define the Nodes
def say_hello(state: SimpleState):
    """A node that adds 'Hello' to the message in the state"""
    print("Executing 'say_hello` node...")
    return {
        "messages": ["Hello"]
    }

def say_world(state: SimpleState):
    """A node that adds 'World' to the message in the state"""
    print("Executing 'say_world` node...")
    return {
        "messages": [" World!"]
    }

# 3. Define Edges
# Since we will be using direct edges and not conditional edges, no need to define functions for them

# 4. Build the Graph
# Instantiate the StateGraph with our defined state.
graph = StateGraph(SimpleState)

# Add your nodes to the graph
graph.add_node("hello_node", say_hello)
graph.add_node("world_node", say_world)

# 5. Connect your nodes with edges

# Begin at the standard START node to connect to your first node
graph.add_edge(START, "hello_node")
# Go from your hello node to your world node
graph.add_edge("hello_node", "world_node")
# Now terminate at the standard END node
graph.add_edge("world_node", END)

# 6. Compile the Graph
graph_runnable = graph.compile()

# 7. Run the Graph

# Create an initial state for the graph to start with.
initial_state = {
    "messages": []
}

final_state = graph_runnable.invoke(initial_state)

print("\n---- Final State ----")
print(final_state)

# Print out the messages
string_messages = [message.content for message in final_state['messages']]
print(f"\n Final list of messages: {string_messages}")

# Draw Graph (install grandalf first)
print(graph_runnable.get_graph().draw_ascii())