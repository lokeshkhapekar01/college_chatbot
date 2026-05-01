from flask import Flask, render_template, request
import json
import random
import sqlite3

app = Flask(__name__)

# Load chatbot intents
with open("intents.json") as file:
    data = json.load(file)

# Create database
def init_db():

    conn = sqlite3.connect("messages.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")

# ABOUT PAGE
@app.route("/about")
def about():
    return render_template("about.html")

# COURSES PAGE
@app.route("/courses")
def courses():
    return render_template("courses.html")

# CONTACT PAGE
@app.route("/contact")
def contact():
    return render_template("contact.html")

# CHATBOT PAGE
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

# SAVE CONTACT MESSAGE
@app.route("/send", methods=["POST"])
def send():

    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = sqlite3.connect("messages.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO messages(name,email,message) VALUES(?,?,?)",
        (name,email,message)
    )

    conn.commit()
    conn.close()

    return "Message Sent Successfully"

# ADMIN PANEL
@app.route("/admin")
def admin():

    conn = sqlite3.connect("messages.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM messages")
    data = cur.fetchall()

    conn.close()

    return render_template("admin.html", data=data)

# CHATBOT RESPONSE
@app.route("/get")
def chatbot_response():

    user_input = request.args.get("msg").lower()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern in user_input:
                return random.choice(intent["responses"])

    return "Sorry I didn't understand. Please ask about fees, courses, admission or contact."

if __name__ == "__main__":
    app.run(debug=True)