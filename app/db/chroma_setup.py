import chromadb

client = chromadb.PersistentClient()

# create collection
client.get_or_create_collection("chunk_embeddings")



