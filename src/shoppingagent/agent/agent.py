from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import uuid

from shoppingagent.agent.tools import search_products_tool, add_to_cart_tool, checkout_tool

load_dotenv()

SYSTEM_PROMPT = """You are a helpful shopping assistant for a grocery store.
You can search products, add items to the cart, and checkout on the user's behalf.

IMPORTANT — grounding rules:
- Only state facts about a product that come directly from the search tool's results (name, price, category, rating, description).
- Never invent additional details, health claims, certifications, or specifications that were not explicitly returned by the tool.
- If the user asks for more detail than what the tool returned, say plainly that no further details are available, rather than guessing.

Always search for a product first if you don't already know its exact product_id.
Never call checkout unless the user has clearly confirmed they want to complete the purchase.
Be concise and friendly in your replies."""

checkpointer = InMemorySaver()

agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    tools=[search_products_tool, add_to_cart_tool, checkout_tool],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
    middleware=[
        SummarizationMiddleware(
            model="groq:openai/gpt-oss-120b",  # a cheaper/smaller model is common here in production
            trigger=("tokens", 3000),               # summarize once history exceeds ~3000 tokens
            keep=("messages", 10),                  # always keep the last 10 messages word-for-word
        ),
    ],
)


if __name__ == "__main__":
    print("Shopping agent ready. Type 'exit' to quit.\n")

    # One thread_id per running session — every message in this run shares memory
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )
        print("Agent:", result["messages"][-1].content, "\n")