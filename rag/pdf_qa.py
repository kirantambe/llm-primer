
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_ollama import OllamaLLM

# 1. Load the PDF
loader = PyPDFLoader("./hera-pheri.pdf")
pages = loader.load()

# 2. Split the text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(pages)

# 3. Embed the chunks using Sentence Transformers
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Store in vector store (in-memory FAISS or custom store)
vectorstore = FAISS.from_documents(chunks, embedding_model)

# 5. Set up local LLM via Ollama
llm = OllamaLLM(model="qwen3:0.6b")  # or "qwen", "mistral", etc.

user_input = input("🎬 ")

while user_input.lower() != "exit":
    # 6. Search vector store for relevant documents
    docs = vectorstore.similarity_search(user_input, k=3)  # K is the number of documents to retrieve

    # 7. Build prompt
    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = f"""
    Answer based on the document:

    {context}

    Question: {user_input}
    Answer:"""

    # 8. Call Ollama
    response = llm.invoke(prompt)
    print(response)

    user_input = input("🎬 ")