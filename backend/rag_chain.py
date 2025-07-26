# rag_chain.py

from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnableLambda
from ingest import load_or_create_vectorstore



# Load vector DB + retriever
path = "docs/3.pdf"
db = load_or_create_vectorstore(path)
retriever = db.as_retriever(search_kwargs={"k": 3})

# LLaMA 3.2 8B via Ollama
llm = OllamaLLM(model="llama3:8b")



prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("chat_history"),
    ("system", "Use the following context to answer the user's question. If unsure, say 'I don't know'."),
    ("human", "{question}"),
    ("system", "Relevant context:\n{context}")
])
# LCEL chain

rag_chain = (
    RunnableMap({
        "context": RunnableLambda(lambda x: retriever.invoke(x["question"])),
        "chat_history": lambda x: x["chat_history"],
        "question": lambda x: x["question"]
    })
    | prompt
    | llm
    | StrOutputParser()
)

# # Prompt
# prompt = ChatPromptTemplate.from_template("""
# You are a helpful assistant. Use the following context to answer the question.
# If the answer cannot be found in the context, say "I don't know".

# Context:
# {context}

# Question:
# {question}
# """)

# query = "What is this document about?"

# # response = rag_chain.invoke({"question": query})
# # print(response)

# for chunk in rag_chain.stream({"question": query}):
#     print(chunk, end="", flush=True)