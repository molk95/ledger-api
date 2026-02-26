## AI V1 (Semantic Search) - What goes where

DB tables:
- documents: source, content, created_at
- chunks: document_id, chunk_text, embedding(vector), chunk_index

Flow:
1) ingest document -> chunk
2) embed each chunk (Ollama/OpenAI)
3) store chunk + embedding in Postgres (pgvector)
4) search: embed query -> ORDER BY embedding <=> query_vector LIMIT k
5) (optional) RAG: send top chunks + query to LLM -> answer

Why cosine:
- compares meaning (vector direction), not exact words

Why chunking:
- long doc embedding becomes "average"; chunking keeps retrieval specific