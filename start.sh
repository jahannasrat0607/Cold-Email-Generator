#!/bin/bash

# Start ChromaDB server in the background
chroma run --host 0.0.0.0 --port 8000 &

# Start Streamlit app
streamlit run app.py --server.port=8501 --server.address=0.0.0.0