import streamlit as st
import pandas as pd
import re
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect("cluster_error_data.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS errors (ErrorRegex TEXT, ErrorSolution TEXT)"
)
conn.commit()
conn.close()


# Create a cache for the database to avoid reloading on every interaction
@st.cache_data(allow_output_mutation=True)
def load_data(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    df = pd.read_sql("SELECT * FROM errors", conn)
    conn.close()
    return df


def check_known_errors(user_input, df):
    # Check if the regex pattern matches any substring of the user input
    matched_errors = []
    for index, row in df.iterrows():
        regex_pattern = row["ErrorRegex"]
        if re.search(regex_pattern, user_input, re.IGNORECASE):
            matched_errors.append(row["ErrorSolution"])
    return matched_errors


def add_new_error(user_input, solution, database_path):
    # Connect to the SQLite database
    conn_new = sqlite3.connect(database_path)

    # Create a new error entry
    cursor_new = conn_new.cursor()
    cursor_new.execute(
        "INSERT INTO errors (ErrorRegex, ErrorSolution) VALUES (?, ?)",
        (user_input, solution),
    )
    conn_new.commit()

    # Reload the updated data
    df_new = load_data(database_path)
    conn_new.close()

    return df_new


def if_submit_button_clicked(new_error_input, new_error_solution, database_path):
    if new_error_input and new_error_solution:
        add_new_error(new_error_input, new_error_solution, database_path)
        st.success("New error added to the database!")


def main():
    # Streamlit app
    st.set_page_config(
        page_title="Error Message Analyzer",
        page_icon="🚀",
    )

    # Containers
    top = st.container()
    output = st.empty()

    # SQLite database path
    database_path = "cluster_error_data.db"

    # Load the database containing known error patterns, regex patterns, and solutions
    df = load_data(database_path)

    # User input for error message
    with top:
        st.title("Error Message Analyzer")

        # chekc st.session_state.user_input exists
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        st.text_area(
            "Enter your error message:", st.session_state.user_input, key="user_input"
        )

        # Make a button to check the error
        if st.session_state.user_input:
            matched_errors = check_known_errors(st.session_state.user_input, df)
            if matched_errors:
                st.header("Known Error Detected")
                for error_solution in matched_errors:
                    st.write(f"Solution: {error_solution}")
            else:
                st.header("New Error Detected")
                st.write("This error is not in the database. Would you like to add it?")

                # Create a form to submit a new error
                if "new_error_input" not in st.session_state:
                    st.session_state.new_error_input = ""
                if "new_error_solution" not in st.session_state:
                    st.session_state.new_error_solution = ""

                new_error_input = st.text_input(
                    "Error Regex (Edit if necessary):",
                    st.session_state.user_input,
                    key="new_error_input",
                )
                new_error_solution = st.text_input(
                    "Error Solution (Provide a solution for the error):",
                    st.session_state.new_error_solution,
                    key="new_error_solution",
                )
                if st.button("Submit"):
                    if_submit_button_clicked(
                        new_error_input, new_error_solution, database_path
                    )
                    # st.session_state.new_error_input = ""
                    # st.session_state.new_error_solution = ""
                    # st.experimental_rerun()

    if st.button("Reload"):
        st.experimental_rerun()


if __name__ == "__main__":
    main()
