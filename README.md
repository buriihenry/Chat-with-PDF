
# Chat with Documents 🧑‍💻🤖

**Chat with Documents** allows you to upload a PDF document and ask questions about its content. The application uses Llama-3.2 for LLM and HuggingFace embeddings for document indexing and querying. You can chat with the document and get real-time responses.

## Features:
- Upload a PDF document and index it.
- Ask questions related to the content of the uploaded document.
- Clear the chat history.
- Download chat history as a text file.
- Display document analytics like word frequency (powered by Plotly).
- Powered by **Llama-3.2** and **HuggingFace embeddings**.

## Requirements

Before running the application, make sure you have the following software and libraries installed:

- Python 3.8+
- Streamlit (for web interface)
- Plotly (for analytics dashboard)
- Llama-3.2 and HuggingFace (for querying and document embedding)
- Qdrant (for vector storage)
- OpenAI API for language model integration

### Libraries:
- `llama_index`
- `streamlit`
- `plotly`
- `qdrant-client`
- `huggingface_hub`
- `Pillow`
- `uuid`
- `base64`

## Installation Instructions

### Step 1: Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/buriihenry/enhanced-chat-with-docs.git
```

### Step 2: Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies. Run the following commands:

#### On Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
.env\Scriptsctivate
```

### Step 3: Install Dependencies

Install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file yet, you can create one by manually adding the following dependencies:

```
llama_index
streamlit
plotly
qdrant-client
huggingface_hub
Pillow
uuid
base64
```

You can also install individual packages with the following command:

```bash
pip install streamlit plotly llama_index qdrant-client huggingface_hub Pillow
```

### Step 4: Install Ollama Model

You will need the Ollama model (Llama-3.2:1b) for querying. Please make sure to install it. You can find instructions on the [Ollama website](https://ollama.com) if necessary.

### Step 5: Install Qdrant

For local testing, you can run a Qdrant instance using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Alternatively, you can install Qdrant locally (without Docker) using pip:

```bash
pip install qdrant-client
```

### Step 6: Set Up Your Environment Variables

Ensure that your environment has access to Qdrant running on `localhost:6333` and any HuggingFace API keys if required.

## Running the Application Locally

Once you have installed all dependencies and set up the environment, you can run the application locally with Streamlit:

1. Make sure you are in the project directory.
2. Run the following command to start the Streamlit app:

```bash
streamlit run app.py
```

This will launch the application in your web browser at `http://localhost:8501`.


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

## Usage

Once the app is running, you can:

1. **Upload a PDF document** via the file upload option in the sidebar.
2. **Chat with the document**: Type a question in the input box, and the application will respond based on the content of the uploaded document.
3. **View Analytics**: The app will show word frequency analysis for the document you uploaded.
4. **Clear chat history**: Press the “Clear Chat” button to reset the conversation.
5. **Download chat history**: Download the entire chat history in `.txt` format for reference.

### Example:
1. Upload a document, such as a research paper or technical manual.
2. Ask specific questions like:
   - "What is the main topic of this document?"
   - "Can you explain the key findings?"
   - "How does the author define machine learning?"

The model will fetch the relevant context and provide answers.

## Contributing

Feel free to open issues or submit pull requests if you would like to contribute to the project. All contributions are welcome!

### To Do:
- Improve document handling and indexing performance.
- Add support for multiple document types (Word, Text, etc.).
- Add advanced NLP features like summarization and entity recognition.

## License

This project is licensed under the MIT License.

---

Thank you for checking out **Enhanced Chat with Documents**! We hope you enjoy using it. 😊