import socket
import json

from utils.functions import process_prompt


def server():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        
        clients = []
        
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            print(f"Connected by {addr}")
            
            data = conn.recv(1024).decode()
            if not data:
                break
            
            response = process_prompt(data)
            response_json = json.dumps(response)
            
            for client in clients:
                try:
                    client.sendall(response_json.encode())
                except:
                    clients.remove(client)

if __name__ == "__main__":
    server()