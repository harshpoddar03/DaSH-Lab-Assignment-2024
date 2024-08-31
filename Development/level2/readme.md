# AI Question Answering System

This project is a distributed AI-powered question answering system that uses the Groq API to process and respond to a list of predefined questions. It consists of a server that handles API requests and multiple clients that send questions and receive answers.

## Project Structure

- `input.txt`: Contains the list of questions to be processed.
- `keys.yml`: Stores the Groq API key.
- `server.py`: The main server script that processes questions and generates responses.
- `client.py`: The client script that sends questions to the server and receives answers.
- `launch_llm_system.sh`: A bash script to launch the server and multiple clients.
- `requirements.txt`: Lists all the Python dependencies for the project.

## Code Explanation

### server.py

This script sets up a socket server that listens for incoming connections from clients. Here are the key components:

1. It reads the Groq API key from `keys.yml`.
2. The `handle_client` function processes each client request:
   - It receives a prompt from the client.
   - Sends the prompt to the Groq API.
   - Sends the response back to the client.
3. The `run_server` function sets up the socket server and handles incoming connections.
4. The script uses threading to handle multiple clients simultaneously.
5. It implements a graceful shutdown mechanism using signal handling.

### client.py

This script sends prompts to the server and receives responses. Key features include:

1. It reads prompts from the `input.txt` file.
2. The `send_prompt` function handles communication with the server:
   - It sends a prompt to the server.
   - Receives the response and parses it as JSON.
   - Implements retry logic in case of connection failures.
3. The script can process a subset of prompts, allowing for distributed processing.
4. Results are saved to a JSON file named `output-{client_id}.json`.

### launch_llm_system.sh

This bash script automates the process of starting the server and multiple clients:

1. It kills any existing Python processes running the server or client scripts.
2. Starts the server script.
3. Calculates how to distribute the input prompts among three clients.
4. Launches three client instances, each processing a portion of the input file.
5. Waits for all clients to finish before shutting down the server.

## Setup

### Creating a Conda Virtual Environment

1. Install Anaconda or Miniconda if you haven't already.

2. Create a new conda environment:
   ```
   conda create -n ai_qa_system python=3.9
   ```

3. Activate the environment:
   ```
   conda activate ai_qa_system
   ```

### Installing Dependencies

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Setting up the Groq API Key

1. Create a `keys.yml` file in the project root.
2. Add your Groq API key in the following format:
   ```yaml
   GROQ_API_KEY: "your_api_key_here"
   ```

## Usage

1. Ensure your questions are in the `input.txt` file, with each question on a new line.

2. Make the launch script executable:
   ```
   chmod +x launch_llm_system.sh
   ```

3. Run the launch script:
   ```
   ./launch_llm_system.sh
   ```

4. The script will start the server and three client instances. Each client will process a portion of the input file and save its results to a separate JSON file.

5. Once all clients have finished, the server will shut down automatically.

## Output

Each client will generate an output file named `output-client{n}.json`, where `n` is the client number. These files contain an array of objects, each with the following structure:

```json
{
  "Prompt": "The original question",
  "Message": "The AI-generated response",
  "TimeSent": 1234567890,
  "TimeRecvd": 1234567891,
  "Source": "Groq-llama3-8b-8192",
  "ClientID": "client_ip_address"
}
```

## Dependencies

Major dependencies include:
- groq
- PyYAML
- socket (Python standard library)
- json (Python standard library)
- threading (Python standard library)

For a full list of dependencies, refer to the `requirements.txt` file.

## Notes

- The system uses the `llama3-8b-8192` model from Groq for generating responses.
- Ensure you have a stable internet connection when running the system, as it makes API calls to Groq.
- The server runs on localhost (127.0.0.1) on port 9999 by default. Modify the `server.py` file if you need to change these settings.

## Troubleshooting

- If you encounter connection errors, ensure that the server is running and that the port is not being used by another application.
- Check that your Groq API key is correctly set in the `keys.yml` file.
- If the clients are not receiving responses, check the server console for any error messages.
