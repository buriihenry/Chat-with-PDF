import os

import base64
import gc
import random
import tempfile
import time
import uuid

from IPython.display import Markdown, display

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, ServiceContext, SimpleDirectoryReader

import streamlit as st

if "id" not in st.session_state:
    st.session_state.id = str(uuid.uuid4())
    st.session_state.file_cache = {}

session_id = st.session_state.id
client = None

@st.cache_resource
def load_llm():
    llm = Ollama(model="llama3.2:1b", request_timeout=120.0)
    return llm

def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()

def display_pdf(file):
    #Opening file from file path

    st.markdown("### PDF Preview")
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="100%" type="application/pdf"
                        style="height:100vh; width:100%"
                    >
                    </iframe>"""
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

with st.sidebar:
    st.header(f"Add your Documents!")

    uploaded_file = st.file_uploader("choose your '.pdf' file", type="pdf")

    if uploaded_file:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, uploaded_file.name)

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                file_key = f"{session_id}- {uploaded_file.name}"
                st.write("Indexing your document....")

                if file_key not in st.session_state.get('file_cache', {}):

                    if os.path.exists(temp_dir):
                        loader = SimpleDirectoryReader(
                            input_dir= temp_dir,
                            required_exts=[".pdf"],
                            recursive=True
                        )
                    else:
                        st.error('Could not find the file you uploaded, Please check again...')
                        st.stop()
                    docs = loader.load_data()

                    # Setup LLM and embedding model
                    llm=Ollama(model="llama3.2:1b", request_timeout=120.0)
                    embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-large-en-v1.5", trust_remote_code=True)
                    
                    # Create the query Engine, where we use cohere reranker on the fetched nodes
                    Settings.embed_model = embed_model
                    index = VectorStoreIndex.from_documents(docs, show_progress=True)

                    # Create the query Engine, where we use cohere reranker on the fetched nodes
                    Settings.llm = llm
                    query_engine = index.as_query_engine()

                    # ====== Customise prompt template ======
                    promt_template = (
                    "Context information is below.\n"
                    "---------------------\n"
                    "{context_str}\n"
                    "---------------------\n"
                    "Given the context information above I want you to think step by step to answer the query in a crisp manner, incase case you don't know the answer say 'I don't know!'.\n"
                    "Query: {query_str}\n"
                    "Answer: "
                    )
                    qa_prompt_tmpl = PromptTemplate(promt_template)

                    query_engine.update_prompts(
                        {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                    )

                    st.session_state.file_cache[file_key] = query_engine
                else:
                    query_engine = st.session_state.file_cache[file_key]                                        
                     

