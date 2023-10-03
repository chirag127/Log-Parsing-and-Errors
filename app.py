import streamlit as st
import pandas as pd
import re

# Create a cache for the database to avoid reloading on every interaction
@st.cache(allow_output_mutation=True)
def load_data(database_path):
    # Load the CSV database containing known error patterns, regex patterns, and solutions
    return pd.read_csv(database_path)

def check_known_errors(user_input, df):
    # Check if the user input matches known error patterns using regex
    matched_errors = []
    for index, row in df.iterrows():
        regex_pattern = row["Error Regex"]
        if re.search(regex_pattern, user_input, re.IGNORECASE):
            matched_errors.append(row["Error Solution"])
    return matched_errors

def add_new_error(user_input, solution, database_path):
    # Implement the logic to add the new error and its solution to the database here
    # Update the CSV file with the new entry
    new_entry = {"Error Regex": user_input, "Error Solution": solution}
    df = pd.read_csv(database_path)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(database_path, index=False)
    return df

def main():
    # Streamlit app
    st.set_page_config(
        page_title="Error Message Analyzer",
        page_icon="🚀",
    )

    # Containers
    top = st.container()
    output = st.empty()

    # Load the CSV database containing known error patterns, regex patterns, and solutions
    database_path = "cluster_error_data.csv"
    df = load_data(database_path)

    # User input for error message
    with top:
        st.title("Error Message Analyzer")

        user_input = st.text_area("Enter your error message:", height=100, max_chars=5000)

        if user_input:
            matched_errors = check_known_errors(user_input, df)

            if matched_errors:
                st.header("Known Error Detected")
                for error_solution in matched_errors:
                    st.write(error_solution)
            else:
                st.header("New Error Detected")
                st.write("This error is not in the database. Would you like to add it?")

                # Option to add the new error and its solution
                user_input = st.text_input("Error Regex (Edit if necessary):", )
                solution = st.text_input("Error Solution (Provide a solution for the error):", )

                if st.button("Add Error"):
                    if user_input:
                        df = add_new_error(user_input, solution, database_path)
                        st.success("New error added to the database.")

    # Add a reload button to prevent unnecessary reloads
    if st.button("Reload"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
