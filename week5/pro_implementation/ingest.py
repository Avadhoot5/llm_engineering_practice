# Importing the libraries 
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
from chromadb import PersistentClient
from tqdm import tqdm
from litellm import completion
from sentence_transformers import SentenceTransformer
from multiprocessing import Pool
from tenacity import retry, wait_exponential
from App.config import azure_endpoint, api_version, headers
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv(override=True)

# Loading the keys
OPENAI_API_KEY = os.getenv('cd_api_key_backup')
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')

ollama_url = "https://ollama.com"

# Defining the constants
MODEL = "azure/gpt-4.1-nano"
MODEL_OLLAMA = "ollama/gpt-oss:120b-cloud"

DB_NAME = str(Path(__file__).parent.parent / "preprocessed_db")
collection_name = "docs"
embedding_model = "all-MiniLM-L6-v2" # need to update
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "knowledge-base"
AVERAGE_CHUNK_SIZE = 150
wait = wait_exponential(multiplier=1, min=10, max=240)

# No. of parallel processes
WORKERS = 3

# embedding model
emb = SentenceTransformer(embedding_model)

# Pydantic class definitions
class Result(BaseModel):
    page_content: str
    metadata: dict

class Chunk(BaseModel):
    headline: str = Field(
        description="A brief heading for this chunk, typically a few words that are most likely to surfaced in a query."
    )
    summary: str = Field(
        description="A few sentences summarizing the content of this chunk to answer common questions."
    )
    original_text: str = Field(
        description="The original text of this chunk from the provided document, exactly as is, not changed in any way"
    )

    def as_result(self, document):
        metadata = {'source': document['source'], 'type': document['type']}
        page_content = f"{self.headline}\n\n{self.summary}\n\n{self.original_text}"
        return Result(page_content=page_content, metadata=metadata)

class Chunks(BaseModel):
    chunks: list[Chunk]

# Fetch and load the docs
def fetch_documents():
    """A homemade version of the LangChain DirectoryLoader"""

    documents = []

    for folder in KNOWLEDGE_BASE_PATH.iterdir():
        doc_type = folder.name
        for file in folder.rglob('*.md'):
            with open(file, 'r', encoding='utf-8') as fs:
                documents.append({'type': doc_type, 'source': file.as_posix(), 'text': fs.read()})

    print(f"Loaded {len(documents)} documents")
    return documents

# Make the prompt - OpenAI
def make_prompt(document):
    how_many = (len(document['text']) // AVERAGE_CHUNK_SIZE) + 1
    return f"""
You take a document and you split the document into overlapping chunks for a KnowledgeBase.

The document is from the shared drive of a company called Insurellm.
The document is of type: {document['type']}
The document has been retrieved from: {document['source']}

A chatbot will use these chunks to answer questions about the company.
You should divide up the document as you see fit, being sure that the entire document is returned in the chunks - don't leave anything out.
This document should probably be split into {how_many} chunks, but you can have more or less as appropriate.
There should be overlap between the chunks as appropriate; typically about 25% overlap or about 50 words, so you have the same text in multiple chunks for best retrieval results.

For each chunk, you should provide a headline, a summary, and the original text of the chunk.
Together your chunks should represent the entire document with overlap.

Here is the document:

{document["text"]}

Respond with the chunks.
"""

def make_messages(document):
    return [
        {'role': 'user', 'content': make_prompt(document)}
    ]

# Make the prompt - Ollama - gpt_oss
def make_prompt_ollama_cloud(document):
    how_many = (len(document['text']) // AVERAGE_CHUNK_SIZE) + 1
    return f"""
You take a document and you split the document into overlapping chunks for a KnowledgeBase.

The document is from the shared drive of a company called Insurellm.
The document is of type: {document['type']}
The document has been retrieved from: {document['source']}

A chatbot will use these chunks to answer questions about the company.
You should divide up the document as you see fit, being sure that the entire document is returned in the chunks - don't leave anything out.
This document should probably be split into {how_many} chunks, but you can have more or less as appropriate.
There should be overlap between the chunks as appropriate; typically about 25% overlap or about 50 words, so you have the same text in multiple chunks for best retrieval results.

For each chunk, you should provide a headline, a summary, and the original text of the chunk.
Together your chunks should represent the entire document with overlap.

    Return ONLY a JSON object matching this structure:

    {{
        "chunks": [
            {{
                "headline": "string",
                "summary": "string",
                "original_text": "string"
            }}
        ]
    }}

    Do not use Markdown.
    Do not use ```json fences.
    Do not include any text before or after the JSON.

    Here is the document:

    {document["text"]}
"""

def make_messages_ollama(document):
    return [
        {'role': 'user', 'content': make_prompt_ollama_cloud(document)}
    ]

# Process the docs
@retry(wait=wait)
def process_document(document):
    # messages = make_messages_ollama(document)
    # response = completion(model=MODEL_OLLAMA, api_key=OLLAMA_API_KEY, api_base=ollama_url, messages=messages, format='json')

    messages = make_messages(document)
    response = completion(model=MODEL, api_base=azure_endpoint, api_key=OPENAI_API_KEY, api_version=api_version, extra_headers=headers, messages=messages, response_format=Chunks)
    reply = response.choices[0].message.content    
    doc_as_chunks = Chunks.model_validate_json(reply).chunks
    return [chunk.as_result(document) for chunk in doc_as_chunks]

    # use below for openai calls
    # messages = make_messages(document)
    # response = completion(model=MODEL, api_base=azure_endpoint, api_key=OPENAI_API_KEY, api_version=api_version, extra_headers=headers, messages=messages, response_format=Chunks)


def create_chunks(documents):
    """Create chunks using a number of workers in parallel.If you get a rate limit error, set the WORKERS to 1."""

    chunks = []
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [
            executor.submit(process_document, document)
            for document in documents
        ]

        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()
            chunks.extend(result)

    return chunks

def create_embeddings(chunks):
    chroma = PersistentClient(path=DB_NAME)

    if collection_name in [c.name for c in chroma.list_collections()]:
        chroma.delete_collection(collection_name)

    texts = [chunk.page_content for chunk in chunks]
    vectors = emb.encode(texts).tolist()

    collection = chroma.get_or_create_collection(collection_name)

    ids = [str(i) for i in range(len(chunks))]
    metas = [chunk.metadata for chunk in chunks]

    collection.add(ids=ids, metadatas=metas, documents=texts, embeddings=vectors)
    print(f'Vectorstore created with {collection.count()} documents')

if __name__ == "__main__":
    documents = fetch_documents()
    chunks = create_chunks(documents)
    create_embeddings(chunks)
    print("Ingestion complete")
