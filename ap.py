from poe_api_wrapper import PoeApi

client = PoeApi("CN6Yyu36OUZAxL1N-ytjvg==")


def get_chatgpt_answer(question):
    bot_list = ["chinchilla", "gpt3_5","chinchilla_instruct", "capybara","acouchy","llama_2_7b_chat","llama_2_13b_chat","llama_2_70b_chat","code_llama_7b_instruct","code_llama_13b_instruct","code_llama_34b_instruct","upstage_solar_0_70b_16bit"]        for bot in bot_list:

        try:
            for chunk in client.send_message(bot, question):
                pass
            return chunk["text"]
        except Exception as e:
            print(e)
            # raise e

    return "Sorry, I am not able to make automated responses at this time. Please try again later."



if __name__ == "__main__":
    print(get_chatgpt_answer("What is the meaning of life?"))