# agent.py

import os
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool

from tools.get_statement import get_statement_info
from tools.apply_loan import apply_loan_procedure
from tools.block_card import block_card_procedure
from tools.get_support_info import get_support_details
from tools.detect_fraud import classify_fraud_in_input

# Read OpenRouter API key from environment variables
api_key = os.getenv("OPENROUTER_API_KEY")

# --- FIX ---
# Add a check to ensure the API key is loaded.
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found. Please check your .env file.")

# Create LLM instance
llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-3.5-turbo",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api_key
)

# Define tools
tools = [
    Tool(name="ClassifyUserIntent", func=classify_fraud_in_input,
         description="Classifies a user message as benign, inquiry, or suspicious based on fraud potential."),
    Tool(name="ApplyLoan", func=apply_loan_procedure, description="Apply for a bank loan."),
    Tool(name="BlockCard", func=block_card_procedure, description="Block a debit or credit card."),
    Tool(name="SupportInfo", func=get_support_details, description="Provide general support contact information."),
    Tool(name="GetStatement", func=get_statement_info, description="Give information about getting bank statements."),
]

# Memory to store conversation context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    system_message=(
        "You are a professional banking assistant. "
        "Only help with general banking queries. If asked for personal information or sensitive tasks, "
        "explain that authentication is required."
    )
)