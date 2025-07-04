from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
import chromadb

def create_chunks_from_text(text: str) -> list[str]:
## 1. Create chunks from the text
    tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v2-small-en")

    # tokenize the text
    tokens = tokenizer.encode(text, add_special_tokens=False)

    # Chunking parameters
    chunk_size = 512
    overlap = 50

    # Generate chunks using a sliding window
    chunks = []
    # for i in range 0 to len of tokens, increment by chunk size - overlap 
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i:i + chunk_size]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks


def create_embeddings_from_chunks(chunks):
## 2. create embeddings for each chunk
    model = SentenceTransformer("jinaai/jina-embeddings-v2-small-en")

    embeddings = model.encode(chunks)
    print(embeddings)
    return embeddings


def create_query_embedding(query: str, collection: chromadb.Collection, n_results: int):
## return the top n results from the vector database based of the query
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )