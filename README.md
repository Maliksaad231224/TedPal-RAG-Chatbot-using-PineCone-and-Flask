# RAG-TEDPAL-Chatbot 🤖

A Retrieval-Augmented Generation (RAG) based chatbot powered by TEDTALKS scraped from Youtube.

![Python Version](https://img.shields.io/badge/python-3.12.3-blue.svg) [![Flask](https://img.shields.io/badge/flask-3.0.2-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/langchain-0.1.11-orange.svg)](https://python.langchain.com/)
[![Pinecone](https://img.shields.io/badge/pinecone-3.0.1-yellow.svg)](https://www.pinecone.io/)


## Table of Contents

- [Features](#features)
- [Dataset](#dataset)
- [Dataset Description](#dataset-description)
- [Installation](#installation)
- [Usage](#usage)

## Features ✨
- RAG-based conversational AI
- TEDPAL integration for enhanced responses
- Customizable knowledge base
- Easy-to-use interface

## Dataset
Original dataset sourced from Kaggle:  
[TED Talks YouTube Links and Corpus for RAG](https://www.kaggle.com/datasets/awansaad6797/tedtalks-youtube-links-and-corpus-for-rag)


## Dataset Description
The dataset contains the following information about TED Talks:
- YouTube links to TED Talk videos
- Text corpus/transcripts of the talks
- Metadata about each talk (speaker, title, etc.)

## Installation 💻

### Prerequisites
- Python 3.12.3
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Maliksaad231224/TedPal-RAG-Chatbot-using-PineCone-and-Flask.git
   cd TedPal-RAG-Chatbot-using-PineCone-and-Flask

2. Make the Virtual Environment
   For Windows
   ```bash
   python -m venv venv
   python venv/Scripts/activate
   ```
   For Linux
   ```bash
   python3 -m venv venv
   python3 venv/bin/activate


3. Run the app
   For Windows
   ```bash
   python app.py
    ```
   For Linux
    ```bash
    python3 app.py

