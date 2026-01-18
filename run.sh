#!/bin/bash

# Start Backend
echo "Starting Backend on http://127.0.0.1:5000..."
cd backend
python app.py &
BACKEND_PID=$!

# Start Frontend
echo "Starting Frontend on http://localhost:5500..."
cd ../frontend
python3 -m http.server 5500 &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers running!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Open http://localhost:5500 in your browser"
echo ""
echo "To stop both servers, press Ctrl+C"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
