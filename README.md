# rag-server
 RAG pipeline server

 # Setup
 * to run the FastAPI server locally run: `uvicorn app.main:app --reload`
 * got to `http://127.0.0.1:8000/docs` to test endpoints with swaggerUI

# Testing
* to run all unit tests, in root folder call `PYTHONPATH=. pytest`
* run with `-s` option to see program output
* to run a specific file add test file path after option