from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Load questions from questions.json
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Define the list of connected players
players = []

# Track the current question index
current_question_index = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


# Add a variable to keep track of the current question
current_question_index = 0


@app.route('/player')
def player():
    return render_template('player.html', current_question=None)


@socketio.on('player_join')
def player_join(player_name):
    player = {'id': request.sid, 'name': player_name, 'score': 0}
    players.append(player)
    join_room(player_name)
    emit('update_players', players, broadcast=True)

    # Send the current question to the player when they join
    if current_question_index < len(questions):
        question = questions[current_question_index]
        emit('new_question', question)


@socketio.on('connect')
def handle_connect():
    pass  # Handle new connections as needed


@socketio.on('admin_next_question')
def admin_next_question():
    global current_question_index
    if current_question_index < len(questions):
        question = questions[current_question_index]
        current_question_index += 1
        emit('new_question', question, broadcast=True)
    else:
        emit('quiz_completed', broadcast=True)


@socketio.on('player_join')
def player_join(player_name):
    player = {'id': request.sid, 'name': player_name, 'score': 0}
    players.append(player)
    join_room(player_name)
    emit('update_players', players, broadcast=True)


@socketio.on('player_answer')
def player_answer(data):
    player_id = request.sid
    player = next((p for p in players if p['id'] == player_id), None)
    if player:
        selected_option = data['selected_option']
        correct_answer = questions[current_question_index -
                                   1]['correct_answer']
        if selected_option == correct_answer:
            player['score'] += 1
            emit('update_players', players, broadcast=True)
        emit('answer_feedback', {
             'is_correct': selected_option == correct_answer})


if __name__ == '__main__':
    socketio.run(app, debug=True)
