This repository demonstrates the implementation of a chatbot using Pinecone, LlamaIndex, and Gemini, designed to interact with a dataset (like a constitution) and provide insightful responses. The chatbot integrates large language models (LLMs) with an efficient vector search for rapid and accurate responses.

Components Overview
<br>

Pinecone

Purpose: A vector database designed for efficient retrieval of embeddings and managing large-scale, high-dimensional data (vectors).
Usage: It stores, searches, and retrieves vectors (e.g., document embeddings) to power machine learning models. In this project, Pinecone stores and retrieves embeddings generated by the embedding model.
<br>

LlamaIndex (formerly GPT Index)

Purpose: A data framework that facilitates easy interaction between large language models (LLMs) and external data sources like documents, databases, or APIs.
Usage: LlamaIndex helps structure and index documents, allowing models to efficiently interact with large datasets by chunking the data and creating a vector index for fast retrieval.
Core Components:
VectorStoreIndex: Mechanism for indexing documents based on vector embeddings.
StorageContext: Manages the underlying vector store and index creation.
<br>

Gemini

Purpose: A large language model (LLM) used for processing user queries and generating document embeddings.
Usage: Gemini creates embeddings for document chunks, which are stored in Pinecone for fast lookup. It also handles the natural language responses for user queries.
<br>

Steps for Output Generation

1. API Key Setup
Set the Google API key and Pinecone API key in environment variables. This is required for authenticating access to Google Gemini and Pinecone services.

2. Model and Embedding Initialization
Instantiate the Gemini LLM with a timeout and set up the embedding model (GeminiEmbedding). These will be used for generating document embeddings and responding to user queries.
3. Document Loading
Use SimpleDirectoryReader to load documents from a specified directory. The documents are chunked into manageable sizes for processing (using Settings.chunk_size).
4. Pinecone Setup
Initialize the Pinecone client and connect to the specified Pinecone index (e.g., knowledgeagent).
Use PineconeVectorStore to store the document embeddings in the Pinecone vector database.
5. Index Creation
Use the VectorStoreIndex from LlamaIndex to create a searchable index of the documents. This index uses the embeddings stored in Pinecone for efficient search and retrieval.
6. Chat Engine Initialization
Convert the index into a chat engine using index.as_chat_engine(). This engine handles user queries and retrieves relevant document chunks for formulating responses.

![WhatsApp Image 2024-11-26 at 22 42 48_9ae9e33b](https://github.com/user-attachments/assets/3a669689-c22b-46de-99eb-1c3eb20f6c4e)

