import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

Prompt = "Write the Go code for the simple data analysis."
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": Prompt}
    ]
)
print(message.text)