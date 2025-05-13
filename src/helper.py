from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(data):
    loader=DirectoryLoader(data,
                           glob="*.pdf", 
                           loader_cls=PyPDFLoader)
    documents=loader.load()
    return documents

def text_split(extracted_Data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=20)
    text_chunk = text_splitter.split_documents(extracted_Data)
    return text_chunk

def downlaod():
    # Set cache location (matches Docker environment variable)
    os.environ['TRANSFORMERS_CACHE'] = os.getenv('TRANSFORMERS_CACHE', '/app/models')
    
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )