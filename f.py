from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re

app = Flask(__name__)

# Establish a connection to the SQLite database
conn = sqlite3.connect("error_database.db")
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS errors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        regex TEXT,
        reason TEXT,
        solution TEXT
    )
''')
conn.commit()

# Function to check if the entered error matches any regex
def check_error(error_text):
    cursor.execute("SELECT * FROM errors")
    rows = cursor.fetchall()
    for row in rows:
        if re.search(row[2], error_text):
            return (True, row[3], row[4])
    return (False, None, None)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_error = request.form["user_error"]
        is_known, reason, solution = check_error(user_error)
        if is_known:
            return render_template("index.html", is_known=True, reason=reason, solution=solution)
        else:
            return render_template("index.html", is_known=False)
    return render_template("index.html")

@app.route("/add_error", methods=["POST"])
def add_error():
    new_error_name = request.form["error_name"]
    new_error_regex = request.form["error_regex"]
    new_error_reason = request.form["error_reason"]
    new_error_solution = request.form["error_solution"]

    cursor.execute("INSERT INTO errors (name, regex, reason, solution) VALUES (?, ?, ?, ?)",
                   (new_error_name, new_error_regex, new_error_reason, new_error_solution))
    conn.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
