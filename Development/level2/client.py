import socket
import json
import sys

def client(prompt):
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(prompt.encode())
        data = s.recv(4096)
    
    response = json.loads(data.decode())
    
    with open(f'client_{sys.argv[1]}_response.json', 'w') as f:
        json.dump(response, f, indent=2)
    
    print(f"Response saved to client_{sys.argv[1]}_response.json")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py <client_id> <prompt>")
        sys.exit(1)
    
    prompt = ' '.join(sys.argv[2:])
    client(prompt)