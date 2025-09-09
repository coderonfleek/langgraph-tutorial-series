from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# Install langchain-openai
from langchain_openai import ChatOpenAI

# Setup Model
llm = ChatOpenAI(model="gpt-4o")

# Define State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# Define the LLM node

def chat_node(state: AgentState) -> dict:
    """A node that invokes the llm to get a response"""

    conversation_history = state["messages"]

    # Give the LLM the full conversation history
    response = llm.invoke(conversation_history)

    # Return the updated conversation history
    return {
        "messages": response # add_messages will figure this out
    }

# Build the Graph

agent_graph = StateGraph(AgentState)

agent_graph.add_node("chat_node", chat_node)

agent_graph.add_edge(START, "chat_node")
agent_graph.add_edge("chat_node", END)

agent = agent_graph.compile()

"""
---- Running Conversational Turns ----
"""

# Send your first messsage
message1 = HumanMessage(content="Hello there! My name is FK")

# Invoke the graph to get the final state (resulting state)
turn1_state = agent.invoke({
    "messages": message1
})

print("--- Graph State after first turn ---")
print(turn1_state)
print("-"* 30)

# Send your second messsage
message2 = HumanMessage(content="What is your favorite color?")

# Invoke the graph with the current conversation history + the new message
turn2_state = agent.invoke({
    "messages": turn1_state["messages"] + [message2]
})

print("--- Graph State after second turn ---")
print(turn2_state)
print("-"* 30)