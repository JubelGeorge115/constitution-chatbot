import os
import streamlit as st
from pinecone import Pinecone
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up LLM and embedding model using environment variables
llm = Gemini(api_key=os.environ["GOOGLE_API_KEY"])
embed_model = GeminiEmbedding(model_name="models/embedding-001")

# Configure settings for LLM and embeddings
Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 1024

# Initialize Pinecone client
pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Function to load documents and initialize the index in Pinecone
def ingest_documents():
    # Load documents from the specified folder
    documents = SimpleDirectoryReader("data").load_data()

    # Initialize Pinecone index and vector store
    pinecone_index = pinecone_client.Index("knowledgeagent")
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    # Create storage context and index from documents
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    st.success("Documents ingested successfully!")
    return index

# Function to initialize the chat engine
def initialize_app():
    # Ingest documents (if not already ingested)
    if 'index' not in st.session_state:
        st.session_state.index = ingest_documents()

    # Create and return the chat engine
    return st.session_state.index.as_chat_engine()

# Streamlit App UI
st.title("Knowledge Agent Chatbot")
st.write("Ingest documents to the Pinecone index and interact with the Knowledge Agent.")

# Button to trigger document ingestion
if st.button("Ingest Documents"):
    st.session_state.index = ingest_documents()
    st.session_state.chat_engine = st.session_state.index.as_chat_engine()

# Initialize the chat engine only once
if 'chat_engine' not in st.session_state:
    st.session_state.chat_engine = initialize_app()

# Initialize chat history if not present
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.chat_message("user").write(content)
    else:
        st.chat_message("assistant").markdown(content)

# Query input box
text_input = st.text_input("Your Question:")

if text_input:
    if text_input.lower() == "exit":
        st.write("Exiting the chat. Goodbye!")
    else:
        try:
            # Get the response from the chat engine
            response = st.session_state.chat_engine.chat(text_input)
            response_text = response.response

            # Display the response
            st.chat_message("assistant").markdown(response_text)

            # Update chat history
            st.session_state.chat_history.append({"role": "user", "content": text_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.write(f"Error: {str(e)}")

# Optional: Add button to clear chat history
if st.button("Clear Chat"):
    st.session_state.chat_history = []  # Clear the chat history
    st.experimental_rerun()  # Simulate a restart by re-running the script
