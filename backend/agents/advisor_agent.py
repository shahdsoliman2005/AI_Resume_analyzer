import json
import os
import chromadb
from gemini_client import client, EMBEDDING_MODEL_NAME
from llm_client import generate_text

_KB_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge_base.json")

_chroma_client = chromadb.Client()
_collection = _chroma_client.get_or_create_collection(name="career_knowledge_base")

_initialized = False


def _embed(text: str) -> list[float]:
    result = client.models.embed_content(model=EMBEDDING_MODEL_NAME, contents=text)
    return result.embeddings[0].values


def init_knowledge_base():

    global _initialized
    if _initialized or _collection.count() > 0:
        _initialized = True
        return

    with open(_KB_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    for chunk in chunks:
        embedding = _embed(chunk["text"])
        _collection.add(
            ids=[chunk["id"]],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{"category": chunk["category"]}],
        )

    _initialized = True


def retrieve_context(question: str, top_k: int = 3) -> list[str]:
    query_embedding = _embed(question)
    results = _collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0] if results["documents"] else []


def career_advice(question: str) -> str:

    retrieved_chunks = retrieve_context(question)
    context_text = "\n- ".join(retrieved_chunks)

    prompt = f"""
    You are a career advisor. Use the information below only as context for
    your answer, and say plainly if it isn't enough to answer the question:

    Relevant information:
    - {context_text}

    User's question: {question}

    Answer practically and directly, in English.
    """
    return generate_text(prompt)
