
# Chat with documents!

Managing and interacting with large documents or databases can be overwhelming, especially when trying to extract specific information quickly or when working with multiple documents. Traditional search methods often fall short when it comes to context-aware, nuanced information retrieval. The challenge is compounded when users need to analyze documents from various sources, potentially leading to confusion and time-consuming processes.

The Chat with Documents AI application provides an intuitive, conversational interface that allows users to interact with documents and extract information seamlessly. By using advanced document retrieval techniques and AI-powered responses, the assistant can help users navigate complex data, answer specific queries, and even summarize content from large documents.

## Project overview

The Chat with Documents AI is a Retrieval-Augmented Generation (RAG) application designed to enhance document management and interaction. It provides a chatbot interface that allows users to ask questions and retrieve relevant information from documents, all powered by AI

The main use cases include:

1. Interactive Document Queries: Users can ask questions related to the document’s content and receive context-aware, precise answers.
2. Document Summarization: Generate summaries of large documents, highlighting key points.
3. Document Retrieval: Search and retrieve specific sections or details from various documents.
4. Contextual Q&A: Answer user questions in real-time, understanding the context of the documents being queried.
5. Document Management: Manage and interact with multiple documents within a single platform.

## Dataset

The dataset for this application consists of various documents, including text files and PDFs. These documents cover a wide range of topics, and the content varies from technical manuals to research papers. The dataset enables the application to demonstrate the power of conversational AI in document management.

You can find the data in [`document_rag/docs`](document_rag/docs).

## Technologies

- Python 3.12.7
- Docker for containerization
- Hugging Face Transformers for advanced NLP models
- Streaamlit for the web interface
- Ollama/llama3.2:1b as open source LLMs
- OpenAI API for language model integration


## Running the application

- Ensure you have Docker installed on your system.
- Clone this repository to your local machine.
- Navigate to the project directory in your terminal.
- install all necessary libaries 

``` bash
pip install nest-asyncio qdrant-client llama-index huggingface-hub sentence-transformers
```
- install Ollama using the following command:

```bash
sudo snap install ollama
```
or 

```bash
curl -o install_ollama.sh https://ollama.com/install.sh
bash install_ollama.sh
```

### Why You Need Ollama
part of the code looks like this:

```bash
llm = Ollama(model="llama3.2:1b", request_timeout=120.0)
```
- This indicates that the application is set up to use an Ollama model for generating responses based on queries. Without installing Ollama, this part of the code will not function, leading to errors when you try to run it.

### Run Ollama in a Docker Container

- If you want to run Ollama using Docker, you can do so with the following command. This will pull the latest Ollama image and start it in a container

```bash
docker run -d --name ollama -p 11434:11434 -v ollama_volume:/root/.ollama ollama/ollama:latest
```
- after installing the Ollama, we need to pull 'llama3.2:1b' by running the below command

```bash
ollama pull llama3.2:1b
```

# New README update coming 