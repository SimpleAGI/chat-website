import openai
import os
from flask import Flask, render_template, request, jsonify, Response, stream_with_context

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    
    def generate():
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{"role": "user", "content": user_input}],
            stream=True
        )
        
        response_content = ""
        for chunk in response:
            if 'choices' in chunk and len(chunk['choices']) > 0:
                delta = chunk['choices'][0].get('delta', {})
                if 'content' in delta:
                    content = delta['content']
                    response_content += content
                    yield f"data: {response_content}\n\n"
        
    return Response(stream_with_context(generate()), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
