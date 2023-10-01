import streamlit as st
import pandas as pd
import re

# Load the CSV file containing error data (if it exists)
try:
    error_database = pd.read_csv("error_database.csv")
except FileNotFoundError:
    error_database = pd.DataFrame(columns=["id", "name", "regex", "reason", "solution"])

# Function to check if the entered error matches any regex
def check_error(error_text):
    for _, row in error_database.iterrows():
        if re.search(row["regex"], error_text):
            return (True, row["reason"], row["solution"])
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

        # Allow the user to add the error to the CSV database
        new_error_name = st.text_input("Error Name:")
        new_error_regex = st.text_input("Error Regex (in a more generalized form):")
        new_error_reason = st.text_area("Error Reason:")
        new_error_solution = st.text_area("Error Solution:")

        if st.button("Add Error to Database"):
            new_error_id = len(error_database) + 1
            new_error_data = {
                "id": new_error_id,
                "name": new_error_name,
                "regex": new_error_regex,
                "reason": new_error_reason,
                "solution": new_error_solution,
            }
            error_database = error_database.append(new_error_data, ignore_index=True)
            error_database.to_csv("error_database.csv", index=False)
            st.success("Error added to the database.")
            st.text("Refresh the page to check the newly added error.")
