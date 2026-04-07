import os
from datetime import datetime
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
# Route tool results back to agent so LLM can decide next steps (chaining)
builder.add_edge("tools", "agent")

graph = builder.compile()

# ==========================================
# Hàm lưu lịch sử hội thoại
# ==========================================
def save_conversation(conversation_history: list, session_id: str):
    """
    Lưu lịch sử hội thoại vào file markdown trong thư mục chat_log.
    """
    chat_log_dir = Path("test_results")
    chat_log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = chat_log_dir / f"conversation_{session_id}_{timestamp}.md"

    lines = [
        f"# Cuộc hội thoại - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        conversation_history[0]["content"] if conversation_history else "",
        "",
        "## Lịch sử hội thoại",
        "",
    ]

    for msg in conversation_history[1:]:  # bỏ system prompt ở đầu
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        lines.append(f"**{role}:** {content}")
        lines.append("")

    filename.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Đã lưu: {filename}]")


# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy – Trợ lý Du lịch Thông minh")
    print("  Gõ 'quit' để thoát")
    print("=" * 60)

    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    conversation_history = []

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            if conversation_history:
                save_conversation(conversation_history, session_id)
            print("Tạm biệt! Hẹn gặp lại!")
            break

        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [{"role": "human", "content": user_input}]})
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": final.content})
