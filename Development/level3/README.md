# Docker-based AI Question Answering System

This project is a distributed AI-powered question answering system that uses the Groq API to process and respond to a list of predefined questions. It consists of a server that handles API requests and multiple clients that send questions and receive answers, all containerized using Docker.

## Project Structure

- `server.py`: The main server script that processes questions and generates responses.
- `client.py`: The client script that sends questions to the server and receives answers.
- `docker-compose.yml`: Defines the multi-container Docker application.
- `input.txt`: Contains the list of questions to be processed.
- `keys.yml`: Stores the Groq API key (not included in the repository).

## Prerequisites

- Docker and Docker Compose installed on your system
- A valid Groq API key

## Setup

1. Clone this repository to your local machine.

2. Create a `keys.yml` file in the project root with your Groq API key:
   ```yaml
   GROQ_API_KEY: "your_api_key_here"
   ```

3. Ensure that the `input.txt` file contains the questions you want to process.

4. Create an `output` directory in the project root to store the results:
   ```
   mkdir output
   ```

## Usage

1. Build and start the containers:
   ```
   docker-compose up --build
   ```

2. The system will automatically distribute the questions among the three client containers and process them.

3. Once all clients have finished, you can find the results in the `output` directory.

## Components

### Server (server.py)

The server script sets up a socket server that listens for incoming connections from clients. Key features include:

- Reads the Groq API key from `keys.yml`
- Handles multiple client connections using threading
- Processes questions using the Groq API
- Implements an inactivity timeout for automatic shutdown

```python
# Key parts of the server code
def handle_client(conn, addr):
    # ... (handles individual client connections)

def run_server(host='0.0.0.0', port=9999):
    # ... (main server loop)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)
    run_server()
```

### Client (client.py)

The client script sends prompts to the server and receives responses. Key features include:

- Reads a portion of prompts from `input.txt`
- Implements retry logic for connection failures
- Saves results to a JSON file in the shared `output` directory

```python
# Key parts of the client code
def send_prompt(prompt, host='server', port=9999, max_retries=60, delay=5):
    # ... (sends prompt to server and receives response)

if __name__ == "__main__":
    # ... (main client logic)
    for prompt in prompts:
        result = send_prompt(prompt)
        result["ClientID"] = client_id
        results.append(result)
    
    # Save results to output file
```

### Docker Compose (docker-compose.yml)

The Docker Compose file defines the multi-container application, including:

- A server container
- Three client containers, each processing a portion of the input
- A shared network for communication
- Volume mounts for input, output, and API key

```yaml
version: '3'

services:
  server:
    build:
      context: .
      dockerfile: Dockerfile.server
    # ... (server configuration)

  client1:
    build:
      context: .
      dockerfile: Dockerfile.client
    # ... (client1 configuration)

  client2:
    # ... (client2 configuration)

  client3:
    # ... (client3 configuration)

networks:
  app_network:
    driver: bridge
```

## Output

Each client generates an output file named `output-client{n}.json` in the `output` directory. These files contain an array of objects, each with the following structure:

```json
{
  "Prompt": "The original question",
  "Message": "The AI-generated response",
  "TimeSent": 1234567890,
  "TimeRecvd": 1234567891,
  "Source": "Groq-llama3-8b-8192",
  "ClientID": "client{n}"
}
```

## Notes

- The system uses the `llama3-8b-8192` model from Groq for generating responses.
- The server runs on port 9999 inside the Docker network.
- Clients will retry connecting to the server for up to 5 minutes before giving up.
- The server will automatically shut down after 60 seconds of inactivity.

## Troubleshooting

- If containers fail to start, ensure that the required ports are not in use by other applications.
- Check the Docker logs for each container to identify any issues:
  ```
  docker-compose logs server
  docker-compose logs client1
  ```
- Ensure that your `keys.yml` file is properly formatted and contains a valid Groq API key.
