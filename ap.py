from poe_api_wrapper import PoeApi

client = PoeApi("CN6Yyu36OUZAxL1N-ytjvg==")


def get_chatgpt_answer(question):
    for chunk in client.send_message("chinchilla", question):
        pass
    return chunk["text"]


if __name__ == "__main__":
    print(get_chatgpt_answer("What is the meaning of life?"))