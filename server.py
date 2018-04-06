from flask import Flask, request, render_template, redirect, url_for, session, escape

app = Flask(__name__)
app.debug = True

usernames = []
public_messages = []
groups = []

@app.route("/", methods=['GET', 'POST'])
def login():
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
    username = "null"
    if 'username' in session:
        username = session['username']
    else:
        # The user is not logged in. Terminate the server.
        # TODO: Need to handle this more elegantly.
        exit(1)
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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
