#!/bin/bash
# Purpose: Run the FastAPI server with controlled file watching

# Kill any existing uvicorn processes
pkill -f "uvicorn app.main:app" || true

# Run uvicorn with specific reload directories
python3 -m uvicorn app.main:app \
    --reload \
    --port 8000 \
    --reload-dir app \
    --reload-exclude "*.pyc" \
    --reload-exclude "__pycache__" \
    --reload-exclude "tests/*" \
    --reload-exclude "test_*.py" 