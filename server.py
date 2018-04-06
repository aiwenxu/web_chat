from flask import Flask, request, render_template, url_for, session, escape
from helper import check_user_in_chat

app = Flask(__name__)
app.debug = True

usernames = []
public_messages = []
group_to_users = {}
group_to_messages = {}
GROUP_ID = 0

@app.route("/", methods=['GET', 'POST'])
def login():
    # TODO: The username should not be too long.
    if request.method == "POST":
        name = request.form["name"]
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
        print('Logged in as %s' % escape(session['username']))
    else:
        # The user is not logged in. Terminate the server.
        # TODO: Need to handle this more elegantly.
        exit(1)
    return render_template("chat.html")

@app.route("/send_public", methods=['GET', 'POST'])
def send_public():
    username = session['username']
    if request.method == "POST":
        new_message = request.form["message"]
        # TODO: May also want to add a timestamp here.
        public_messages.append(username + ": " + new_message)
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
                # TODO: The quit button in chat.html is not implemented yet.
                return "Please quit the current chat first."
            else:
                if to_user_in_chat == 0:
                    global GROUP_ID
                    GROUP_ID += 1
                    group_to_users[GROUP_ID] = [from_user, to_user]
                    group_to_messages[GROUP_ID] = []
                else:
                    group_to_users[to_user_in_chat].append(from_user)
            print(group_to_users)
            return "Connection successful!"

@app.route("/send_private", methods=['GET', 'POST'])
def send_private():
    username = session['username']
    chat_num = check_user_in_chat(username, group_to_users)
    if chat_num == 0:
        return "Unsuccessful. You have no private chat connection."
    if request.method == "POST":
        new_message = request.form["message"]
        # TODO: May also want to add a timestamp here.
        group_to_messages[chat_num].append(username + ": " + new_message)
        print(group_to_messages[chat_num])
        return "Successfully sent!"

@app.route("/receive_private", methods=['GET', 'POST'])
def receive_private():
    username = session['username']
    chat_num = check_user_in_chat(username, group_to_users)
    if chat_num == 0:
        return "You have no private chat connection."
    if request.method == "GET":
        # TODO: If we have a timestamp, we can filter out the earlier messages.
        info = [group_to_users[chat_num], group_to_messages[chat_num]]
        return(str(info))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
