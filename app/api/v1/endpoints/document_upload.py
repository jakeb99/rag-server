from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz
import app.services.documents.parser as parser
import app.services.embedding.embedding as embedder
import chromadb
from chromadb.utils import embedding_functions

router = APIRouter(prefix="/document_upload")

# chromadb stuff

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="jinaai/jina-embeddings-v2-small-en"
)

client = chromadb.PersistentClient()
collection = client.get_or_create_collection("embeddings", embedding_function=sentence_transformer_ef)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # print(file.content_type)
    match file.content_type:
        case "application/pdf":
            text = await parser.parse_pdf(file)
        case _:
            raise HTTPException(status_code=400, detail="Unsupported file type")

    # split text into chunks
    chunks = embedder.create_chunks_from_text(text)
    # create embeddings for each chunk
    embeddings = embedder.create_embeddings_from_chunks(chunks)

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    # query_embedding = embedder.create_query_embedding("What is model view controller?")

    # print(query_embedding)

    # for embedding_chunk in embeddings:
    #     print(f"chunk: {embedding_chunk}\n")

    # return content
    return {
        "chunks": len(chunks),
        "embeddings": len(embeddings)
    }

@router.post("/query/")
async def query(query: str, n_results: int):

    result = embedder.create_query_embedding(query, collection, n_results)

    return {"results": result}