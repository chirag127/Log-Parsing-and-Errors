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
with st.form(key='error_form'):
    user_error = st.text_area("Enter your error message:")
    submit_button = st.form_submit_button("Check Error")

if submit_button:
    is_known, reason, solution = check_error(user_error)
    if is_known:
        st.success("This is a known error.")
        st.write("Reason:", reason)
        st.write("Solution:", solution)
    else:
        st.error("This is a new error.")
        st.write("You can add this error to the database below:")

        # Define a callback function for updating the output
        def update_output():
            # Clear the previous output
            output.empty()
            # Check if all the inputs are filled
            if new_error_name and new_error_regex and new_error_reason and new_error_solution:
                # Add the error to the database
                cursor.execute("INSERT INTO errors (name, regex, reason, solution) VALUES (?, ?, ?, ?)",
                           (new_error_name, new_error_regex, new_error_reason, new_error_solution))
                conn.commit()
                # Display a success message
                output.success("Error added to the database.")
                output.text("Refresh the page to check the newly added error.")
            else:
                # Display an error message
                output.error("Please fill all the inputs.")

        # Allow the user to add the error to the database
        with st.form(key='add_error_form'):
            # Create input widgets with on_change parameter
            new_error_name = st.text_input("Error Name:", on_change=update_output)
            new_error_regex = st.text_input("Error Regex (in a more generalized form):", on_change=update_output)
            new_error_reason = st.text_area("Error Reason:", on_change=update_output)
            new_error_solution = st.text_area("Error Solution:", on_change=update_output)
            # Create an empty placeholder for the output
            output = st.empty()
