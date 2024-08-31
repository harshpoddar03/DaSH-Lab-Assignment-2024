import socket
import json
import sys
import uuid
import time

def send_prompt(prompt, host='localhost', port=9999, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(30)  # Increased timeout
                sock.connect((host, port))
                sock.sendall(prompt.encode('utf-8'))
                
                # Receive the response in chunks
                chunks = []
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
                
                response = b''.join(chunks).decode('utf-8')
                
                # Try to parse the JSON response
                try:
                    return json.loads(response)
                except json.JSONDecodeError as json_err:
                    print(f"JSON Decode Error: {json_err}")
                    print(f"Received response: {response}")
                    raise
        except (ConnectionResetError, socket.timeout) as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Giving up.")
                raise

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python client.py <input_file> <start_line> <end_line> <client_id>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    start_line = int(sys.argv[2])
    end_line = int(sys.argv[3])
    client_id = sys.argv[4]
    
    with open(input_file, 'r') as f:
        all_prompts = f.read().splitlines()
    
    # Select the portion of prompts for this client
    prompts = all_prompts[start_line-1:end_line]
    
    results = []
    for prompt in prompts:
        result = send_prompt(prompt)
        result["ClientID"] = client_id
        
        # # Simulate receiving responses from other clients
        # if uuid.uuid4().int % 2 == 0:
        #     result["Source"] = "user"
        
        results.append(result)
    
    output_filename = f'output-{client_id}.json'
    with open(output_filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {output_filename}")