from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)

# Load the CSV database containing known error patterns, regex patterns, and solutions
database_path = "cluster_error_data.csv"
df = pd.read_csv(database_path)

def check_known_errors(user_input):
    # Check if the user input matches known error patterns using regex
    matched_errors = []
    for index, row in df.iterrows():
        regex_pattern = row["Error Regex"]
        if re.search(regex_pattern, user_input, re.IGNORECASE):
            matched_errors.append(row["Error Solution"])
    return matched_errors

def add_new_error(user_input, solution):
    # Implement the logic to add the new error and its solution to the database here
    # Update the CSV file with the new entry
    new_entry = {"Error Regex": user_input, "Error Solution": solution}
    global df
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(database_path, index=False)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        matched_errors = check_known_errors(user_input)

        if matched_errors:
            return render_template("result.html", matched_errors=matched_errors)
        else:
            return render_template("add_error.html", user_input=user_input)

    return render_template("index.html")

@app.route("/add_error", methods=["POST"])
def add_error():
    user_input = request.form["user_input"]
    solution = request.form["solution"]
    add_new_error(user_input, solution)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
