import time
import yaml
from groq import Groq
import socket


def read_api_key():
    with open('keys.yml', 'r') as file:
        keys = yaml.safe_load(file)
    return keys.get('GROQ_API_KEY')

client = Groq(
    api_key=read_api_key()
)

def find_available_port(start_port=65432):
    for port in range(start_port, 65535):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    raise RuntimeError("No available ports")

def process_prompt(prompt, client_id):
    print(f"Processing prompt from client {client_id}: {prompt}")
    time_sent = int(time.time())
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        
        time_received = int(time.time())
        
        response = {
            "Prompt": prompt,
            "Message": chat_completion.choices[0].message.content,
            "TimeSent": time_sent,
            "TimeRecvd": time_received,
            "Source": "Groq-llama3-8b-8192",
            "ClientID": client_id
        }
        print(f"Response generated for client {client_id}")
        return response
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return {
            "Prompt": prompt,
            "Message": f"Error processing prompt: {str(e)}",
            "TimeSent": time_sent,
            "TimeRecvd": int(time.time()),
            "Source": "Error",
            "ClientID": client_id
        }