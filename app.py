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
    ai_response = get_ai_response(user_input)
    return jsonify({'ai_response': ai_response})

def get_ai_response(user_input):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    # Ensure to replace 'your-actual-api-key-here' with your real OpenAI API key.
    response = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": user_input}],
    )
    return response.choices[0].message['content'].strip()

if __name__ == '__main__':
    app.run(debug=True)
