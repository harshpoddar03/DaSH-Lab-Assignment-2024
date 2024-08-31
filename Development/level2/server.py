import socket
import json
import time
from groq import Groq
import yaml
import threading
import signal

# Global flag to indicate if the server should continue running
running = True

def read_api_key():
    with open('keys.yml', 'r') as file:
        keys = yaml.safe_load(file)
    return keys.get('GROQ_API_KEY')

client = Groq(api_key=read_api_key())

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    data = conn.recv(1024).strip()
    prompt = data.decode('utf-8')
    client_id = addr[0]
    
    time_sent = int(time.time())
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    
    time_received = int(time.time())
    
    response_data = {
        "Prompt": prompt,
        "Message": chat_completion.choices[0].message.content,
        "TimeSent": time_sent,
        "TimeRecvd": time_received,
        "Source": "Groq-llama3-8b-8192",
        "ClientID": client_id
    }
    
    conn.sendall(json.dumps(response_data).encode('utf-8'))
    conn.close()

def run_server(host='localhost', port=9999):
    global running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        s.settimeout(1)  # Set a timeout for the accept() call
        print(f"Server running on {host}:{port}")
        
        while running:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
            except socket.timeout:
                continue  # This allows checking the running flag periodically

def shutdown_server(signum, frame):
    global running
    print("Shutting down server...")
    running = False

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)
    run_server()
    print("Server has shut down.")