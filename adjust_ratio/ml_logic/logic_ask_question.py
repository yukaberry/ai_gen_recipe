from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI

# Load documents (e.g., local text files with cooking tips)
documents = SimpleDirectoryReader("data").load_data()

# Create a vector index
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(llm=OpenAI())

response = query_engine.query("How do I adjust a cake recipe if I only have 2 eggs instead of 3?")
print(response)
