import streamlit as st
from pymongo import MongoClient
import re
from poe_api_wrapper import PoeApi
from streamlit_extras.app_logo import add_logo

client = PoeApi("SkSETIfxASyu3DtxwlkdnA==")


def get_chatgpt_answer(question):
    # bot_list = ["chinchilla", "gpt3_5","chinchilla_instruct", "capybara","acouchy","llama_2_7b_chat","llama_2_13b_chat","llama_2_70b_chat","code_llama_7b_instruct","code_llama_13b_instruct","code_llama_34b_instruct","upstage_solar_0_70b_16bit"]

    bot_list = ["chinchilla", "gpt3_5","chinchilla_instruct", "capybara"]
    for bot in bot_list:

        try:
            for chunk in client.send_message(bot, question):
                pass
            return chunk["text"]
        except Exception as e:
            print(e)
            # raise e

    return "Sorry, I am not able to make automated responses at this time. Please try again later."

def logo():
    add_logo("https://lh3.googleusercontent.com/YtXTsa-6SaaMl02-OUo8iRztlX5Thu4aCLavunIV1M5hm9y4ySTPpMjpY44fL4ayz7Se", height=300)
# Access MongoDB connection details from Streamlit secrets
db_uri = st.secrets["db_uri"]
db_database = st.secrets["db_database"]
db_collection = st.secrets["db_collection"]

client = MongoClient(db_uri)


dblist = client.list_database_names()
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
        page_icon="https://lh3.googleusercontent.com/YtXTsa-6SaaMl02-OUo8iRztlX5Thu4aCLavunIV1M5hm9y4ySTPpMjpY44fL4ayz7Se",
    )

    # Containers
    top = st.container()

    logo()


    # User input for error message
    with top:

        # Add logo

        # Add title
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
                for error_solution, i in zip(
                    matched_errors, range(len(matched_errors))
                ):
                    # Display the error solution in a good format
                    st.write(f"Solution {i+1}:", error_solution)
            else:
                st.header("New Error Detected")
                st.write("This error is not in the database. Would you like to add it?")

                # # get the answer from chatgpt
                # answer = get_chatgpt_answer("please suggest a regex and a solution for this error: " + st.session_state.user_input)

                # # Display the answer
                # st.write("suggested regex and solution: " + answer)

                # add a spinner while waiting for the answer
                with st.spinner(
                    "Please wait while we suggest a regex and a solution for this error ..."
                ):
                    if "chatgpt_answer" not in st.session_state:
                        st.session_state.chatgpt_answer = ""
                        # get the answer from chatgpt

                        try:

                            answer = get_chatgpt_answer(
                            f"""please suggest a regex for the following error and a brief solution to solve the following error:

{st.session_state.user_input}

just provide the two values in the following format:
Regex: <regex>

Solution: <solution>


don't provide any other information in the message, just the regex and the solution. Thank you!"""
                        )
                            st.session_state.chatgpt_answer = answer
                            # print("suggested regex and solution: \n " + st.session_state.chatgpt_answer )
                        except Exception as e:

                            print("error" + str(e))

                            st.write("Error in auto-suggesting a regex and a solution for this error. Please provide a regex and a solution manually.")

                    # Display the answer
                    # st.write("suggested regex and solution: " + answer)



                if "new_error_input" not in st.session_state:
                    st.session_state.new_error_input = ""
                if "new_error_solution" not in st.session_state:
                    st.session_state.new_error_solution = ""

                # try: to extract the regex and solution from the answer

                try:
                    regex = re.search(
                        r"Regex:(.*)\n", st.session_state.chatgpt_answer
                    ).group(1)
                    solution = re.search(
                        r"Solution: (.*)\n", st.session_state.chatgpt_answer
                    ).group(1)

                    # remove the code block from the regex from the start and end if exists
                    regex = re.sub(r"`", "", regex)

                    st.session_state.new_error_input = regex
                    st.session_state.new_error_solution = solution
                except Exception as e:
                    print("error" + str(e))

                    # print("the chatgpt answer is: ", st.session_state.chatgpt_answer)

                    # st.write("Error in auto-suggesting a regex and a solution for this error. Please provide a regex and a solution manually.")

                    if len(st.session_state.chatgpt_answer) > 0:
                        st.write("suggested regex and solution: \n " + st.session_state.chatgpt_answer)


                    # print("error in extracting the regex and solution from the answer")

                new_error_input = st.text_input(
                    "Error Regex (Edit if necessary):",
                    key="new_error_input",
                )
                new_error_solution = st.text_input(
                    "Error Solution (Provide a solution for the error):",
                    key="new_error_solution",
                )

                if st.button("Submit"):
                    if_submit_button_clicked(new_error_input, new_error_solution)


if __name__ == "__main__":
    main()
