from flask import Flask, render_template
from flask_socketio import SocketIO, join_room
from flask_login import login_required, LoginManager, current_user
from DBase import DB
from backP.UserLogin import  UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QkrejD'
socketio=SocketIO(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id_user):
    return UserLogin().fromDB(id_user, DB())


from AuthPart import auth_bp

# @app.route('/get_users')
# @login_required
# def get_users():
#     users = DB().getUsers()
#     users = [user[0] for user in users if user[0] != current_user.get_user()[0]]
#     return jsonify(users)

@app.route('/private/<username>')
@login_required
def private_chat(username):
    return render_template("private.html", username=username)

@socketio.on('join_private')
def handle_join_private(data):
    room = f"private_{data['to']}_{data['from']}"
    join_room(room)
    print(f"User {current_user.get_user()[1]} joined room {room}")

@socketio.on('private_message')
def handle_private_message(data):
    sender = current_user.get_user()[1]
    receiver = data['to']
    room = f"private_{receiver}_{sender}"
    socketio.emit('private_message', f"{sender}: {data['message']}", room=room)

@socketio.on('message')
def handle_message(msg):
    msg=f"{current_user.get_user()[1]}:"+msg
    socketio.send(msg)

@app.route('/chat')
@login_required
def chat():
    users = DB().getUsers()
    users = [user for user in users if user[0] != current_user.get_user()[0]]
    return render_template("index.html", users=users)

app.register_blueprint(auth_bp)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True, port=5000)