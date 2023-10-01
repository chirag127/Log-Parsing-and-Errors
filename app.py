import streamlit as st
import sqlite3
import re

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

# Streamlit app
st.title("Error Handler")

# User input for error
user_error = st.text_area("Enter your error message:")

if st.button("Check Error"):
    is_known, reason, solution = check_error(user_error)
    if is_known:
        st.success("This is a known error.")
        st.write("Reason:", reason)
        st.write("Solution:", solution)
    else:
        st.error("This is a new error.")
        st.write("You can add this error to the database below:")

        # Initialize the values in session state
        if "new_error_name" not in st.session_state:
            st.session_state.new_error_name = ""
        if "new_error_regex" not in st.session_state:
            st.session_state.new_error_regex = ""
        if "new_error_reason" not in st.session_state:
            st.session_state.new_error_reason = ""
        if "new_error_solution" not in st.session_state:
            st.session_state.new_error_solution = ""

        # Use session state to store and access the values of the widgets
        new_error_name = st.text_input("Error Name:", value=st.session_state.new_error_name, on_change=st.session_state.update, args=("new_error_name",))
        new_error_regex = st.text_input("Error Regex (in a more generalized form):", value=st.session_state.new_error_regex, on_change=st.session_state.update, args=("new_error_regex",))
        new_error_reason = st.text_area("Error Reason:", value=st.session_state.new_error_reason, on_change=st.session_state.update, args=("new_error_reason",))
        new_error_solution = st.text_area("Error Solution:", value=st.session_state.new_error_solution, on_change=st.session_state.update, args=("new_error_solution",))

        if st.button("Add Error to Database"):
            # Add the error to the database
            cursor.execute("INSERT INTO errors (name, regex, reason, solution) VALUES (?, ?, ?, ?)",
                           (new_error_name, new_error_regex, new_error_reason, new_error_solution))
            conn.commit()
            st.success("Error added to the database.")
            st.text("Refresh the page to check the newly added error.")
