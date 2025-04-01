from src.helper import load_pdf, text_split, downlaod
from pinecone import Pinecone, ServerlessSpec 
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY

extracted = load_pdf(data='/home/malik-saad-ahmed/Desktop/Desktop/Learnings/Medical Chatbot RAG/RAG-Medical-Chatbot-Main/Medical_Chatbot_Using_Gale_Encyclopedia_of_Medicine/data/preprocessed_TEDTALKS.pdf')
text_chunks= text_split(extracted)
embeddings = downlaod()

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name= 'TEDTALKS'

pc.create_index(
    name=index_name,
    dimension=384,
    metric='cosine',
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

docsearch =  PineconeVectorStore.from_existing_index(
    index_name= index_name,
    embedding=embeddings,
    documents = text_chunks
)

