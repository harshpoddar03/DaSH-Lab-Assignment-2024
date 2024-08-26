import json
import os
import time
from groq import Groq
import yaml

# open input.txt
with open('input.txt', 'r') as f:
    data = f.read()

def read_api_key():
    with open('keys.yml', 'r') as file:
        keys = yaml.safe_load(file)
    return keys.get('GROQ_API_KEY')

client = Groq(
    api_key=read_api_key()
)

def process_prompts(data_list):
    results = []
    for prompt in data_list:
        time_sent = int(time.time())  # Current time as UNIX timestamp
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        
        time_received = int(time.time())  # Time after receiving the response
        
        response_data = {
            "Prompt": prompt,
            "Message": chat_completion.choices[0].message.content,
            "TimeSent": time_sent,
            "TimeRecvd": time_received,
            "Source": "Groq-llama3-8b-8192"
        }
        
        results.append(response_data)
    
    return results


data = data.split('\n')
data_list = []
for i in data:
    data_list.append(i)

print("Starting to process prompts...")

# Process all prompts
all_results = process_prompts(data_list)

print("Finished processing prompts.")

# Save results to a JSON file
with open('output.json', 'w') as f:
    json.dump(all_results, f, indent=2)
    
print("Results saved to output.json")

