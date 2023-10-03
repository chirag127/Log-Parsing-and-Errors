import streamlit as st
from pymongo import MongoClient
import re
import tomli

# Access MongoDB connection details from Streamlit secrets
db_uri = st.secrets["db_uri"]
db_database = st.secrets["db_database"]
db_collection = st.secrets["db_collection"]

# # Connect to MongoDB using configuration
# client = MongoClient(config["mongodb"]["uri"])
# db = client[config["mongodb"]["database"]]  # Connect to the specified database

# # Ensure the collection exists, create it if it doesn't
# collection_name = config["mongodb"]["collection"]
# if collection_name not in db.list_collection_names():
#     db.create_collection(collection_name)

# collection = db[collection_name]

# Connect to MongoDB using secrets
client = MongoClient(db_uri)


dblist = myclient.list_database_names()
print("the list of databases are: ", dblist)

if db_database in dblist:
  print("The database exists.")

  db = client[db_database]  # Connect to the specified database

else:
  print("The database does not exist.")

  db = client[db_database]  # Connect to the specified database


# Ensure the collection exists, create it if it doesn't
collection_name = db_collection
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

collection = db[collection_name]



def check_known_errors(user_input):
    # Check if the regex pattern matches any document in the MongoDB collection
    matched_errors = []
    for error_doc in collection.find():
        regex_pattern = error_doc["ErrorRegex"]
        if re.search(regex_pattern, user_input, re.IGNORECASE):
            matched_errors.append(error_doc["ErrorSolution"])
    return matched_errors

def add_new_error(user_input, solution):
    # Insert a new document into the MongoDB collection
    error_doc = {"ErrorRegex": user_input, "ErrorSolution": solution}
    collection.insert_one(error_doc)


def if_submit_button_clicked(new_error_input, new_error_solution):
    if new_error_input and new_error_solution:
        add_new_error(new_error_input, new_error_solution)
        st.success("New error added to the database!")

def main():
    # Streamlit app
    st.set_page_config(
        page_title="Error Message Analyzer",
        page_icon="🚀",
    )

    # Containers
    top = st.container()

    # User input for error message
    with top:
        st.title("Error Message Analyzer")

        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        st.text_area(
            "Enter your error message:", st.session_state.user_input, key="user_input"
        )

        if st.button("Check Error") or st.session_state.user_input:
            matched_errors = check_known_errors(st.session_state.user_input)
            if matched_errors:
                st.success("Known Error Detected")
                for error_solution , i in zip(matched_errors, range(len(matched_errors))):

                    # Display the error solution in a good format
                    st.write(f"Solution {i+1}:" , error_solution)
            else:
                st.header("New Error Detected")
                st.write("This error is not in the database. Would you like to add it?")

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
                        new_error_input, new_error_solution
                    )

if __name__ == "__main__":
    main()
