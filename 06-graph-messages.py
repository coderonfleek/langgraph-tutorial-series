from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# --- 1. Define the Agent State ---
# We subclass the prebuilt MessagesState class.
# This gives us a 'messages' key with the add_messages reducer already set.
# We can then add any other state variables we need.
class MyGraphState(MessagesState):
    turn_count: int

# --- 2. Define the Nodes ---
# This node simulates a human's message.
# It returns a dictionary with the new message to be appended to the state.
def user_node(state: MyGraphState) -> dict:
    print("Executing user_node...")
    # The new HumanMessage will be appended by the add_messages reducer.
    return {"messages": HumanMessage(content="What's the weather like today?")}

# This node simulates an AI's response.
# It accesses the full message history from the state to provide context.
def ai_node(state: MyGraphState) -> dict:
    print("Executing ai_node...")
    # We can access messages just like a list or dictionary.
    last_human_message = state["messages"][-1]
    
    # Simulate a response based on the last message.
    response_content = f"I've received your query: '{last_human_message.content}'. " \
                       "I can't tell you the weather right now, but I can confirm that my code is working!"
    
    # Return the new AIMessage to be appended.
    return {"messages": AIMessage(content=response_content)}

# This node demonstrates that we can update other state variables
# alongside the message history.
def counter_node(state: MyGraphState) -> dict:
    print("Executing counter_node...")
    return {"turn_count": state["turn_count"] + 1}


# --- 3. Build the Graph ---
# We define our workflow as a simple state machine.
graph = StateGraph(MyGraphState)
    
# Add our nodes to the graph.
graph.add_node("user_input", user_node)
graph.add_node("ai_response", ai_node)
graph.add_node("increment_counter", counter_node)

# Connect the nodes to define the flow of execution.
# The flow is sequential: START -> user -> ai -> counter -> END.
graph.add_edge(START, "user_input")
graph.add_edge("user_input", "ai_response")
graph.add_edge("ai_response", "increment_counter")
graph.add_edge("increment_counter", END)

agent = graph.compile()

# Invoke the graph with an initial state.
initial_state = {"turn_count": 0}
    
final_state = agent.invoke(initial_state)

print("\n--- Final State of the Graph ---")
print(final_state)
print("\n")