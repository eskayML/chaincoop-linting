from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from groq import Groq


load_dotenv()
app = Flask(__name__)

client = Groq(
    # This is the default and can be omitted
    api_key=os.getenv("GROQ_API_KEY"),
)



@app.route('/chat', methods=['POST'])
def chat():


    full_code = request.get_data(as_text = True)
    PROMPT = f'''You are a python code linting tool, your goal is to show the mistakes in the python syntax when provided with a code, 
but  without actually showing the output of the code
Now, given the python code below, write a very brief info about the mistake.

```python
{full_code}
```
'''

    
    if not full_code:
        return jsonify({'error': 'No message provided'}), 400

    

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": PROMPT,
        }
    ],
    model="llama-3.1-70b-versatile",
    )

    return jsonify({"response" : chat_completion.choices[0].message.content})


if __name__ == '__main__':
    app.run(debug=True)
