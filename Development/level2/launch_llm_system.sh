#!/bin/bash

# Kill any existing Python processes
pkill -f "python server.py"
pkill -f "python client.py"

# Start the server
python server.py &
SERVER_PID=$!

# Wait for the server to start
sleep 5

# Get the total number of lines in the input file
TOTAL_LINES=$(wc -l < input.txt)

# Calculate lines per client (assuming 3 clients)
LINES_PER_CLIENT=$((TOTAL_LINES / 3))

# Run multiple clients with specific portions of the input file
python client.py input.txt 1 $LINES_PER_CLIENT client1 &
CLIENT1_PID=$!
sleep 2
python client.py input.txt $((LINES_PER_CLIENT + 1)) $((LINES_PER_CLIENT * 2)) client2 &
CLIENT2_PID=$!
sleep 2
python client.py input.txt $((LINES_PER_CLIENT * 2 + 1)) $TOTAL_LINES client3 &
CLIENT3_PID=$!

# Wait for all clients to finish
wait $CLIENT1_PID
wait $CLIENT2_PID
wait $CLIENT3_PID

# Send SIGTERM to the server
kill -TERM $SERVER_PID

# Wait for the server to shut down (give it up to 10 seconds)
wait $SERVER_PID

echo "All clients finished and server has been shut down. Combined output saved to combined_output.json"