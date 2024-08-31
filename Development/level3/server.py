import socket
import json
import time
from groq import Groq
import yaml
import threading
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global flag to indicate if the server should continue running
running = True
last_activity = time.time()
INACTIVITY_TIMEOUT = 60  # Shutdown after 60 seconds of inactivity

def read_api_key():
    with open('keys.yml', 'r') as file:
        keys = yaml.safe_load(file)
    return keys.get('GROQ_API_KEY')

client = Groq(api_key=read_api_key())

def handle_client(conn, addr):
    global last_activity
    logger.info(f"New connection from {addr}")
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
    last_activity = time.time()

def run_server(host='0.0.0.0', port=9999):
    global running, last_activity
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        s.settimeout(1)  # Set a timeout for the accept() call
        logger.info(f"Server running on {host}:{port}")
        
        while running:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
            except socket.timeout:
                if time.time() - last_activity > INACTIVITY_TIMEOUT:
                    logger.info("Server inactive for too long. Shutting down...")
                    running = False
                continue  # This allows checking the running flag periodically

def shutdown_server(signum, frame):
    global running
    logger.info("Shutting down server...")
    running = False

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)
    run_server()
    logger.info("Server has shut down.")