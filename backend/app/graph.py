from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import sqlite3
from .tools import tools
from langgraph.prebuilt import ToolNode,tools_condition

load_dotenv()

AK=os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=AK
)
 
#tool binding
llm=llm.bind_tools(tools)
tool_node=ToolNode(tools)

#state
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatState)   

graph.add_node('chat_node',chat_node)
graph.add_node("tools",tool_node)

graph.add_edge(START,'chat_node')
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools", "chat_node") 
graph.add_edge('chat_node',END)



chatbot=graph.compile(checkpointer=checkpointer)

