"""
Agent module - Core logic for the RAG Agent.
Separates agent logic from the chat interface.
"""

from openai import OpenAI
from dotenv import load_dotenv

from tools import search
from prompt import build_system_prompt, build_user_prompt, format_context, DEFAULT_TONE

load_dotenv()

# Configuration
CHAT_MODEL = "gpt-5-nano-2025-08-07"

# Initialize OpenAI client
client = OpenAI()


class Agent:
    """
    RAG Agent that processes user queries with context from the knowledge base.
    """
    
    def __init__(self, tone: str = None):
        """
        Initialize the agent.
        
        Args:
            tone: The tone/personality instruction for the agent
        """
        self.tone = tone or DEFAULT_TONE
        self.conversation_history = []
    
    def process(self, user_input: str, use_rag: bool = True) -> str:
        """
        Process a user input and generate a response.
        
        This is the main flow:
        1. Search the knowledge base for relevant context
        2. Build the prompt with tone + context + question
        3. Call the LLM
        4. Return the response
        
        Args:
            user_input: The user's question or message
            use_rag: Whether to search the knowledge base (default: True)
        
        Returns:
            The agent's response
        """
        # Step 1: Search for relevant context
        retrieved_context = ""
        if use_rag:
            search_results = search(user_input, top_k=3)
            retrieved_context = format_context(search_results)
        
        # Step 2: Build prompts
        system_prompt = build_system_prompt(
            tone=self.tone,
            retrieved_context=retrieved_context
        )
        user_prompt = build_user_prompt(user_input)
        
        # Step 3: Build messages for the API
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history for context
        messages.extend(self.conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_prompt})
        
        # Step 4: Call the LLM
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_prompt})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Keep history manageable (last 10 exchanges)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return assistant_message
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def set_tone(self, tone: str) -> None:
        """
        Set a new tone for the agent.
        
        Args:
            tone: The new tone instruction
        """
        self.tone = tone
