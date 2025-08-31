from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
import random

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# --- AI-like Dummy Productivity Tips ---
def get_productivity_tip():
    tips = [
        "Take a 5-minute break after every 1 hour of work.",
        "Start your day with the most important task.",
        "Use the Pomodoro technique to stay focused.",
        "Review your tasks at the end of the day.",
        "Avoid multitasking for better productivity."
    ]
    return random.choice(tips)

# --- Routes ---
@app.route("/")
def index():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    tip = get_productivity_tip()
    return render_template("index.html", tasks=tasks, tip=tip)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    deadline = request.form["deadline"]
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, deadline, status) VALUES (?, ?, ?)", (title, deadline, "Pending"))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", ("Completed", task_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
