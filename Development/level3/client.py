import socket
import json
import sys
import time
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_prompt(prompt, host='server', port=9999, max_retries=60, delay=5):
    for attempt in range(max_retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(30)  # Increased timeout
                sock.connect((host, port))
                logger.info(f"Connected to server on attempt {attempt + 1}")
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
                    logger.error(f"JSON Decode Error: {json_err}")
                    logger.error(f"Received response: {response}")
                    raise
        except (ConnectionRefusedError, socket.timeout) as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error("Max retries reached. Giving up.")
                raise

if __name__ == "__main__":
    if len(sys.argv) < 5:
        logger.error("Usage: python client.py <input_file> <start_line> <end_line> <client_id>")
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
        results.append(result)
    
    output_filename = f'output-{client_id}.json'
    output_path = os.path.join('/app/output', output_filename)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to {output_path}")
    logger.info(f"Client {client_id} finished processing. Exiting.")
    sys.exit(0)