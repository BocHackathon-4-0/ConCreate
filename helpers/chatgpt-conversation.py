import openai
import json
import os


# Set up your API key
openai.api_key = os.environ.get("OPENAI_TOKEN", "")




def get_info_from_user():
    messages = [
        {"role": "system", "content": "You are a friendly assistant that tries to collect information about the user, you need to collect and verify the legal name of the user"},
    ]

    while True:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        assistant_msg = response["choices"][0]["message"]["content"]
        print(f"Assistant: {assistant_msg}")

        messages.append({"role": "assistant", "content":assistant_msg})

        user_message = input(">")
        messages.append({"role": "user", "content":user_message})

        messages_to_json = [x for x in messages]
        messages_to_json.append({"role": "system", "content": "Generate a json string with the key name and the legal name of the user as a value. If name not given yet, put null a value"})
        
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_to_json
        )

        # print("\ncheck if data was extracted\n")
        message =  response["choices"][0]["message"]["content"]

        result = {"name": None}
        try:
            result = json.loads(message)
        except:
            result = {"name": None}

        print(result)

