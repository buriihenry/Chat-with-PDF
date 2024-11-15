import os
import base64
import gc
import tempfile
import uuid
import streamlit as st
from datetime import datetime
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import plotly.express as px
import pandas as pd

# ====== Initial Setup ======
if "id" not in st.session_state:
    st.session_state.id = str(uuid.uuid4())
    st.session_state.file_cache = {}
    st.session_state.messages = []

session_id = st.session_state.id

# ====== Caching LLM & Embedder ======
@st.cache_resource
def load_models():
    llm = Ollama(model="llama3.2:1b", request_timeout=120.0)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5", trust_remote_code=True)
    return llm, embed_model

# ====== Function to Display PDF ======
def display_pdf(file):
    st.markdown("### PDF Preview 📄")
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"
            style="border:none;"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

# ====== Analytics Dashboard ======
def display_analytics(data):
    st.markdown("## Document Analytics 📊")
    word_counts = {}
    for doc in data:
        doc_text = doc.text  # Accessing the 'text' attribute of the Document object
        for word in doc_text.split():
            word_counts[word] = word_counts.get(word, 0) + 1
    
    df = pd.DataFrame(list(word_counts.items()), columns=['Word', 'Frequency']).nlargest(10, 'Frequency')
    fig = px.bar(df, x='Word', y='Frequency', title='Top 10 Word Frequencies')
    st.plotly_chart(fig)

# ====== Reset Chat ======
def reset_chat():
    st.session_state.messages = []
    gc.collect()

# ====== Download Chat History ======
def download_chat():
    chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    st.download_button("💾 Download Chat History", chat_history, file_name="chat_history.txt")

# ====== Sidebar for Document Upload ======
with st.sidebar:
    st.title("📚 Chat with Documents")
    st.info("Upload a PDF document and ask questions about its content.")
    st.markdown("Powered by **Llama-3.2** and **HuggingFace embeddings**.")
    
    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

    if uploaded_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            file_key = f"{session_id}-{uploaded_file.name}"
            if file_key not in st.session_state.file_cache:
                with st.spinner("🔄 Indexing your document, please wait..."):
                    try:
                        loader = SimpleDirectoryReader(input_dir=temp_dir, required_exts=[".pdf"], recursive=True)
                        docs = loader.load_data()
                        
                        llm, embed_model = load_models()
                        Settings.embed_model = embed_model
                        index = VectorStoreIndex.from_documents(docs, show_progress=True)
                        
                        Settings.llm = llm
                        query_engine = index.as_query_engine()

                        prompt_template = (
                            "Context information is below.\n"
                            "---------------------\n"
                            "{context_str}\n"
                            "---------------------\n"
                            "Answer the question using the context above. If the answer is unknown, respond with 'I don't know'.\n"
                            "Query: {query_str}\n"
                            "Answer: "
                        )
                        qa_prompt_tmpl = PromptTemplate(prompt_template)
                        query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})
                        
                        st.session_state.file_cache[file_key] = query_engine
                        st.success("✅ Document indexed successfully!")
                        display_pdf(uploaded_file)
                        display_analytics(docs)
                    except Exception as e:
                        st.error(f"Error during indexing: {e}")
                        st.stop()
            else:
                query_engine = st.session_state.file_cache[file_key]

# ====== Main UI ======
st.title("🤖 Chat with Your Documents")
st.markdown("""
    Welcome to **Chat with Docs**! 📚
    
    **Features**:
    - Upload a PDF document via the sidebar.
    - Ask questions about the document content below.
    - View analytics of the most frequent words.
    - Download your chat history as a text file.
""")

st.button("🔄 Clear Chat", on_click=reset_chat)

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with st.chat_message(role):
        st.markdown(f"**[{timestamp}]** {message['content']}")

# ====== Chat Input ======
if prompt := st.chat_input("Ask a question about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            query_engine = st.session_state.file_cache[file_key]
            streaming_response = query_engine.query(prompt)
            full_response = streaming_response.response
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = f"An error occurred: {e}"
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ====== Download Button ======
download_chat()
