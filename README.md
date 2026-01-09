# Agents

Repositório para o curso/disciplinas sobre criação de agentes inteligentes.

Sumário
- O que é machine learning?
- O que é um agente?
- O que é um embedding?
- O que é um sistema de inferência?
- Como fazer uma requisição ao serviço?
- Como criar um embedding de um texto ou arquivo?
- Como armazenar isso em um local para consultas futuras?
- Como o agente consulta essa base?

## O que é machine learning?
Machine learning (aprendizado de máquina) é um subcampo da inteligência artificial que cria modelos capazes de aprender padrões a partir de dados e fazer previsões ou tomar decisões sem serem explicitamente programados para cada caso. Exemplos incluem regressão, classificação, redes neurais e aprendizado por reforço.

## O que é um agente?
Um agente é um sistema que percebe seu ambiente (por meio de sensores), toma decisões internamente (usando políticas, modelos ou regras) e age sobre o ambiente (por meio de atuadores). Exemplos: chatbots, robôs, agentes de busca e sistemas autônomos.

## O que é um embedding?
Embedding é uma representação vetorial de itens (como textos, sentenças, imagens) em um espaço contínuo onde a similaridade semântica é preservada: itens semanticamente próximos ficam próximos no espaço vetorial.

## O que é um sistema de inferência?
Um sistema de inferência é o componente que usa modelos (por exemplo, modelos de linguagem, classificadores ou regras) para gerar conclusões, respostas ou decisões a partir de entradas e contexto recuperado.

## Como fazer uma requisição ao serviço?
Exemplo mínimo (assumindo um serviço HTTP/REST):
1. Gerar embedding:
   POST /embed
   Body: { "text": "Seu texto aqui" }
2. Buscar por similaridade:
   POST /search
   Body: { "query": "Como criar um agente?", "top_k": 5 }

Exemplo de cliente em Python:

```python
import requests
r = requests.post("http://localhost:8000/embed", json={"text":"Olá mundo"})
print(r.json())
```

## Como criar um embedding de um texto ou arquivo?
Passos gerais:
1. Extrair texto do arquivo (PDF, DOCX, TXT) se necessário.
2. Utilizar um modelo de embeddings (ex.: sentence-transformers) para transformar o texto em vetor.
3. Normalizar e armazenar o vetor junto com metadados.

Exemplo (Python + sentence-transformers):

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode("Texto de exemplo", normalize_embeddings=True)
```

## Como armazenar isso em um local para consultas futuras?
Opções:
- FAISS (indexador vetorial local)
- Serviços gerenciados: Pinecone, Weaviate, Milvus
- Banco de dados com suporte a vetores: PostgreSQL + pgvector
- Arquivos locais (npz/parquet) para projetos pequenos

Formato mínimo para cada item:
- id, texto, vetor (float32), metadata (JSON), timestamp

## Como o agente consulta essa base?
Fluxo:
1. Agente recebe uma query do usuário.
2. Gera embedding para a query.
3. Realiza busca por similaridade (top-k) na base vetorial.
4. Recupera documentos/contexto relevantes.
5. Usa um modelo de linguagem (ou regras) para gerar resposta considerando o contexto.

Exemplo resumido em Python:

```python
# 1. gerar embedding
q_vec = model.encode(query, normalize_embeddings=True)
# 2. buscar top-k
docs = vector_index.search(q_vec, top_k=5)
# 3. construir prompt e gerar resposta
prompt = build_prompt(query, docs)
response = llm.generate(prompt)
```
