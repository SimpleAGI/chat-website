from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*', manage_session=True)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    session_id = request.sid
    send({'msg': 'User connected', 'sid': session_id})

@socketio.on('user_message')
def handle_user_message(json_msg):
    print('User Message: ' + str(json_msg))
    response = {'msg': json_msg.get('msg'), 'sid': json_msg.get('sid')}
    send(response, broadcast=True)
    # Simulate an AI response after processing the user message
    ai_response = {'msg': f"AI responds to {json_msg.get('msg')}", 'sid': 'AI'}
    socketio.emit('ai_message', ai_response)

if __name__ == '__main__':
    socketio.run(app)