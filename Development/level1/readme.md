# AI Question Answering System

This project is an AI-powered question answering system that uses the Groq API to process and respond to a list of predefined questions.

## Project Structure

- `input.txt`: Contains the list of questions to be processed.
- `keys.yml`: Stores the Groq API key.
- `output.json`: The output file containing the processed responses.
- `requirement.txt`: Lists all the Python dependencies for the project.
- `script.py`: The main Python script that processes the questions and generates responses.

## Setup

1. Ensure you have Python installed on your system.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Groq API key:
   - Create a `keys.yml` file in the project root.
   - Add your Groq API key in the following format:
     ```yaml
     GROQ_API_KEY: "your_api_key_here"
     ```

## Usage

1. Add your questions to the `input.txt` file, with each question on a new line.

2. Run the script:
   ```
   python script.py
   ```

3. The script will process each question and save the responses in `output.json`.

## Output Format

The `output.json` file contains an array of objects, each with the following structure:

```json
{
  "Prompt": "The original question",
  "Message": "The AI-generated response",
  "TimeSent": 1234567890,
  "TimeRecvd": 1234567891,
  "Source": "Groq-llama3-8b-8192"
}
```

For a full list of dependencies, refer to the `requirements.txt` file.

## Notes

- The script uses the `llama3-8b-8192` model from Groq for generating responses.
- Ensure you have a stable internet connection when running the script, as it makes API calls to Groq.
