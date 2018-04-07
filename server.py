from flask import Flask, request, render_template, url_for, session, escape
from helper import check_user_in_chat, get_timestamp

app = Flask(__name__)
app.debug = True

usernames = []
public_messages = []
group_to_users = {}
group_to_messages = {}
GROUP_ID = 0
user_states_in_private_chat = {}

@app.route("/", methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        name = request.form["name"]

        if len(name) >= 50:
            return "Please enter a shorter username."

        if name == "":
            return "Username cannot be empty."
        elif name in usernames:
            return "Username unavailable."
        else:
            usernames.append(name)
            session['username'] = name
            print(url_for("chat"))
            return "Success! <a href='/chat'>Enter the chat room.</a>"

    return render_template("login.html")

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if 'username' in session:
        username = session['username']
        print('Logged in as %s' % escape(username))
        public_messages.append(username + " has joined the chat!")
        return render_template("chat.html")

@app.route("/get_name", methods=['GET'])
def get_name():
    return session['username']

@app.route("/send_public", methods=['GET', 'POST'])
def send_public():
    username = session['username']
    if request.method == "POST":
        new_message = request.form["message"]
        current_time = get_timestamp()
        public_messages.append(username + ": " + new_message + " [" + current_time + "]")
        print(public_messages)
        return "Successfully sent!"

@app.route("/receive_public", methods=['GET', 'POST'])
def receive_public():
    if request.method == "GET":
        info = [usernames, public_messages]
        return(str(info))

@app.route("/join_chat", methods=['GET', 'POST'])
def join_chat():
    if request.method == "POST":
        from_user = session['username']
        to_user = request.form["to_user"]
        if from_user == to_user:
            return "Cannot connect to yourself."
        else:
            from_user_in_chat = check_user_in_chat(from_user, group_to_users)
            to_user_in_chat = check_user_in_chat(to_user, group_to_users)
            if from_user_in_chat != 0:
                return "Please quit the current chat first."
            else:
                if to_user_in_chat == 0:
                    global GROUP_ID
                    GROUP_ID += 1
                    group_to_users[GROUP_ID] = [from_user, to_user]
                    group_to_messages[GROUP_ID] = []
                    user_states_in_private_chat[from_user] = 0
                    user_states_in_private_chat[to_user] = 0
                else:
                    group_to_users[to_user_in_chat].append(from_user)
                    user_states_in_private_chat[from_user] = len(group_to_messages[to_user_in_chat])
                    group_to_messages[to_user_in_chat].append(from_user + " has joined the chat!")
            print(group_to_users)
            return "Connection successful!"

@app.route("/quit_chat", methods=['GET', 'POST'])
def quit_chat():
    if request.method == "GET":
        username = session['username']
        chat_num = check_user_in_chat(username, group_to_users)
        if chat_num == 0:
            return "Quit unsuccessful. You are not in any private chat."
        else:
            group_to_users[chat_num].remove(username)
            group_to_messages[chat_num].append(username + " has left the chat!")
            if len(group_to_users[chat_num]) == 1:
                group_to_users.pop(chat_num, None)
                group_to_messages.pop(chat_num, None)
            print(group_to_users)
            return "Quit successful."

@app.route("/send_private", methods=['GET', 'POST'])
def send_private():
    username = session['username']
    chat_num = check_user_in_chat(username, group_to_users)
    if chat_num == 0:
        return "Unsuccessful. You have no private chat connection."
    if request.method == "POST":
        new_message = request.form["message"]
        current_time = get_timestamp()
        group_to_messages[chat_num].append(username + ": " + new_message + " [" + current_time + "]")
        print(group_to_messages[chat_num])
        return "Successfully sent!"

@app.route("/receive_private", methods=['GET', 'POST'])
def receive_private():
    username = session['username']
    chat_num = check_user_in_chat(username, group_to_users)
    if chat_num == 0:
        return "You have no private chat connection."
    if request.method == "GET":
        user_state = user_states_in_private_chat[username]
        info = [group_to_users[chat_num], group_to_messages[chat_num][user_state:]]
        return(str(info))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
