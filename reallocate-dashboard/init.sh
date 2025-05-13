#!/bin/bash

# Start the FastAPI backend
echo "Starting FastAPI backend..."
uvicorn backend:app --host 0.0.0.0 --port 8000 &

# # Wait until the backend is up and running
# echo "Waiting for backend to start..."
# until curl -s http://localhost:8000/docs > /dev/null; do
#   sleep 2
# done

echo "Backend is running!"
sleep 10
# Start Streamlit
echo "Starting Streamlit app..."
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
