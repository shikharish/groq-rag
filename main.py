from collections import deque
import json
import os
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
from llama_index.readers.web import SimpleWebPageReader

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

links = []
with open("links.json", "r") as file:
    links = json.load(file)

n_links = 1
documents = SimpleWebPageReader(html_to_text=True).load_data(links[0:n_links])

text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
nodes = text_splitter.get_nodes_from_documents(documents, show_progress=True)

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

llm = Groq(model="gemma2-9b-it", api_key=GROQ_API_KEY)
Settings.llm = llm
Settings.embed_model = embed_model
vector_index = VectorStoreIndex.from_documents(
    documents, show_progress=True, embed_model=embed_model, node_parser=nodes
)

vector_index.storage_context.persist(persist_dir="./storage_mini")
storage_context = StorageContext.from_defaults(persist_dir="./storage_mini")
index = load_index_from_storage(storage_context, llm=llm)
query_engine = index.as_query_engine(llm=llm)


def pipeline(context, query):
    context_str = " ".join(context)
    full_query = f"Context: {context_str}\nQuery: {query}"
    response = query_engine.query(full_query)
    return response

context = deque()
while True:
    query = input("$ ")
    if query == r"\q":
        break
    response = pipeline(context=context, query=query)
    print(f"> {response}")

    if len(context) > 10:
        context.popleft()
    context.append(f"{response}")
