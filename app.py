import openai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    return jsonify(stream_chat(user_input))

async def stream_chat(user_input):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    # Ensure to replace 'your-actual-api-key-here' with your real OpenAI API key.
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": user_input}],
        stream=True
    )
    response_content = ""
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            response_content += delta['content']
            yield jsonify({'ai_response': response_content})

if __name__ == '__main__':
    app.run(debug=True)
