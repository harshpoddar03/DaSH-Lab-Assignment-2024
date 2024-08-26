import time
import yaml
from groq import Groq


def read_api_key():
    with open('keys.yml', 'r') as file:
        keys = yaml.safe_load(file)
    return keys.get('GROQ_API_KEY')

client = Groq(
    api_key=read_api_key()
)

def process_prompt(prompt):
    time_sent = int(time.time())
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    
    time_received = int(time.time())
    
    return {
        "Prompt": prompt,
        "Message": chat_completion.choices[0].message.content,
        "TimeSent": time_sent,
        "TimeRecvd": time_received,
        "Source": "Groq-llama3-8b-8192"
    }
