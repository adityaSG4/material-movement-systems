#!/bin/bash

echo "Starting WareVision Application..."

# Activate virtual environment
source myenv/bin/activate

# Install dependencies if not already installed
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found!"
    exit 1
fi

pip install -r requirements.txt

# Start both backend servers in the background
echo "Starting object detection server..."
python object_detection.py &
OBJECT_DETECTION_PID=$!

echo "Starting maze solver server..."
python maze_solver.py &
MAZE_SOLVER_PID=$!

# Wait for servers to initialize
sleep 2

# Start the frontend server
echo "Starting frontend server..."
python -m http.server 8000 &
HTTP_SERVER_PID=$!

# Function to cleanup background processes
cleanup() {
    echo "Shutting down servers..."
    kill $OBJECT_DETECTION_PID 2>/dev/null
    kill $MAZE_SOLVER_PID 2>/dev/null
    kill $HTTP_SERVER_PID 2>/dev/null
    exit 0
}

# Set up cleanup on script termination
trap cleanup SIGINT SIGTERM

echo "All servers started!"
echo "Access the application at: http://localhost:8000"

# Keep the script running
wait
