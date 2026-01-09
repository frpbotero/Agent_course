"""
Prompt templates for the RAG Agent.
Contains system and user prompt templates with placeholders for:
- Tone instruction
- Retrieved context
- User question
"""

SYSTEM_PROMPT_TEMPLATE = """{tone_instruction}

## Contexto Recuperado
{retrieved_context}

## Instruções
- Use o contexto acima para enriquecer sua resposta quando relevante
- Se não houver contexto relevante, responda com seu conhecimento geral
- Seja claro e direto nas suas respostas
- Mantenha o foco na pergunta do usuário
"""

USER_PROMPT_TEMPLATE = "{user_question}"

# Default tone
DEFAULT_TONE = "Você é um assistente prestativo e direto. Responda de forma clara e objetiva."


def build_system_prompt(tone: str = None, retrieved_context: str = None) -> str:
    """
    Build the system prompt with tone and context.
    
    Args:
        tone: The tone instruction for the agent
        retrieved_context: The context retrieved from the knowledge base
    
    Returns:
        Formatted system prompt
    """
    tone = tone or DEFAULT_TONE
    
    if not retrieved_context:
        retrieved_context = "Nenhum contexto relevante encontrado na base de conhecimento."
    
    return SYSTEM_PROMPT_TEMPLATE.format(
        tone_instruction=tone,
        retrieved_context=retrieved_context
    )


def build_user_prompt(user_question: str) -> str:
    """
    Build the user prompt.
    
    Args:
        user_question: The user's question
    
    Returns:
        Formatted user prompt
    """
    return USER_PROMPT_TEMPLATE.format(user_question=user_question)


def format_context(search_results: list[dict]) -> str:
    """
    Format search results into a readable context string.
    
    Args:
        search_results: List of search results from the search tool
    
    Returns:
        Formatted context string
    """
    if not search_results:
        return ""
    
    context_parts = []
    for i, result in enumerate(search_results, 1):
        source_info = f" (Fonte: {result['source']})" if result.get('source') else ""
        context_parts.append(f"[{i}]{source_info}: {result['text']}")
    
    return "\n\n".join(context_parts)
