Agente de Console com RAG (Retrieval-Augmented Generation)
Construir um agente de terminal com capacidade de chat, ingestão de documentos (embeddings) e busca semântica. O agente utiliza RAG para enriquecer as respostas.

Arquitetura Proposta
Storage
Tools
Core
Console
chat.pyInterface do Terminal
agent.pyLógica do Agente
prompt.pyTemplates
ingestEmbedding + Storage
searchBusca Semântica
knowledge_base.jsontexto → embedding
Proposed Changes
Tools Layer
[NEW] 
tools.py
Implementar as ferramentas do agente:

ingest(text: str, source: str = None)

Gera embedding do texto usando a API do Google
Armazena em knowledge_base.json como {text, embedding, source, timestamp}
Retorna confirmação
search(query: str, top_k: int = 3)

Gera embedding da query
Calcula similaridade de cosseno com todos os embeddings armazenados
Retorna os top_k textos mais relevantes
load_knowledge_base() / save_knowledge_base()

Funções auxiliares para persistência em JSON
Prompt Layer
[NEW] 
prompt.py
Templates estruturados:

SYSTEM_PROMPT = """
{tone_instruction}
## Contexto Recuperado
{retrieved_context}
## Instruções
- Use o contexto acima para enriquecer sua resposta
- Se não houver contexto relevante, responda com seu conhecimento geral
- Seja claro e direto
"""
USER_PROMPT = "{user_question}"
Agent Layer
[NEW] 
agent.py
Lógica central do agente:

Agent class

__init__(tone: str) - Configura o tom do agente
process(user_input: str) - Fluxo principal:
Faz busca no knowledge base
Monta o prompt com tom + contexto + pergunta
Chama a LLM (Google Gemini)
Retorna a resposta
Integração com tools

ingest_document(text, source) - Wrapper para a tool de ingest
search_knowledge(query) - Wrapper para a tool de search
Chat Layer
[NEW] 
chat.py
Interface de terminal:

Loop principal de chat

Prompt interativo com readline
Comandos especiais:
/ingest <texto> - Ingere texto diretamente
/ingest_file <caminho> - Ingere arquivo
/search <query> - Busca direta (sem chat)
/clear - Limpa histórico
/exit ou /quit - Sair
Formatação rica

Cores para diferenciar usuário/agente
Indicador de "pensando..."
Configuration
[NEW] 
config.py
Arquivo de configuração:

Tom padrão do agente
Caminho do knowledge base
Parâmetros de busca (top_k)
Dependencies
[MODIFY] 
requirements.txt
google-generativeai>=0.3.0
numpy
python-dotenv
NOTE

O arquivo será renomeado para requirements.txt (typo no nome atual)

User Review Required
IMPORTANT

Qual modelo do Google deseja usar?

gemini-1.5-flash (mais rápido, mais barato)
gemini-1.5-pro (mais capaz)
IMPORTANT

Qual tom/personalidade o agente deve ter por padrão? Exemplo: "Você é um assistente técnico prestativo e direto. Responda de forma clara e objetiva."

Verification Plan
Manual Testing
Testar ingestão:

python chat.py
# No chat:
/ingest Este é um documento de teste sobre Python
/ingest Python é uma linguagem de programação versátil
Testar busca direta:

/search linguagem programação
# Deve retornar os textos relevantes
Testar chat com RAG:

# Perguntar algo relacionado ao conteúdo ingerido
O que você sabe sobre Python?
# A resposta deve usar o contexto recuperado
Verificar persistência:

# Sair e reabrir
/exit
python chat.py
/search Python
# Deve encontrar os documentos anteriores
