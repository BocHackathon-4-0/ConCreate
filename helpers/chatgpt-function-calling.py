import openai
import json
from typing import List, Optional
from pydantic import BaseModel
import os


# Set up your API key
openai.api_key = os.environ.get("OPENAI_TOKEN", "")




class Erc20AIResponse(BaseModel):
    name: Optional[str]
    symbol: Optional[str]
    owner: Optional[str]
    premint: Optional[int]
    mintable: Optional[bool]
    burnable: Optional[bool]
    pausable: Optional[bool]
    # votes: Optional[bool]


schema = Erc20AIResponse.model_json_schema()




null_object = Erc20AIResponse(name=None, symbol=None, owner=None, premint=None, mintable=None, burnable=None, pausable=None).model_dump_json()

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        # {"role": "system", "content": f"You are a friendly assistant that asks the user for information to fill the json {null_object} about an ERC20 deployment"},
        {"role": "system", "content": f"""You are a friendly assistant that needs to fill the json {null_object}. The information should be given by the user. The information is about an ERC20 smart contract."""},
        {"role": "assistant", "content": "What is the name of the ERC20 smart contract?"},
        {"role": "user", "content": "My contract name should be KOKOSPOROSICOIN"},
        {"role": "assistant", "content": "What is the symbol for the ERC20 smart contract?"},
        {"role": "user", "content": "My contract name should be KPC"},
        {"role": "assistant", "content": "Who will be the owner of the ERC20 smart contract?"},
        {"role": "user", "content": "Why do you need this information?"},
        {"role": "assistant", "content": "The owner of the ERC20 smart contract is the address that will have special administrative privileges, such as the ability to change contract parameters, mint new tokens, or perform other administrative functions."},
        {"role": "user", "content": "Ah, I see, the contract owner will be me"},
        {"role": "assistant", "content": "What is your wallet address?"},
        {"role": "user", "content": "The address is Faneromenis 23, Nicosia, Cyprus"},
        {"role": "assistant", "content": "I apologize for the misunderstanding. The owner of the ERC20 smart contract should be a wallet address, which is typically represented as a string of alphanumeric characters. Could you please provide a valid wallet address as the owner of the contract?"},
        {"role": "user", "content": "0xF80214FD406294c2A44ef7A1D548793e12Ae8E5c"},
        {"role": "assistant", "content": "How many tokens would you like to pre-mint for the ERC20 smart contract?"},
        {"role": "user", "content": "100"},
        {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be mintable?"},
        {"role": "user", "content": "Yes please"},
        {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be burnable?"},
        {"role": "user", "content": "No"},
        {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be pausable?"},
        {"role": "user", "content": "No, not really"},
        
    ]
)
assistant_msg = response["choices"][0]["message"]["content"]
print(f"Assistant: {assistant_msg}")

print(json.dumps([
        # {"role": "system", "content": f"You are a friendly assistant that asks the user for information to fill the json {null_object} about an ERC20 deployment"},
        {"role": "system", "content": f"""You are a friendly assistant that needs to fill the json {null_object}. The information should be given by the user. The information is about an ERC20 smart contract."""},
        {"role": "assistant", "content": "What is the name of the ERC20 smart contract?"},
        {"role": "user", "content": "My contract name should be KOKOSPOROSICOIN"},
        {"role": "assistant", "content": "What is the symbol for the ERC20 smart contract?"},
        {"role": "user", "content": "My contract name should be KPC"},
        {"role": "assistant", "content": "Who will be the owner of the ERC20 smart contract?"},
        {"role": "user", "content": "Why do you need this information?"},
        {"role": "assistant", "content": "The owner of the ERC20 smart contract is the address that will have special administrative privileges, such as the ability to change contract parameters, mint new tokens, or perform other administrative functions."},
        {"role": "user", "content": "Ah, I see, the contract owner will be me"},
        {"role": "assistant", "content": "What is your wallet address?"},
        {"role": "user", "content": "The address is Faneromenis 23, Nicosia, Cyprus"},
        {"role": "assistant", "content": "I apologize for the misunderstanding. The owner of the ERC20 smart contract should be a wallet address, which is typically represented as a string of alphanumeric characters. Could you please provide a valid wallet address as the owner of the contract?"},
        {"role": "user", "content": "0xF80214FD406294c2A44ef7A1D548793e12Ae8E5c"},
        {"role": "assistant", "content": "How many tokens would you like to pre-mint for the ERC20 smart contract?"},
        {"role": "user", "content": "100"},
        {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be mintable?"},
        {"role": "user", "content": "Yes please"},
        {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be burnable?"},
        {"role": "user", "content": "No"},
        {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be pausable?"},
        {"role": "user", "content": "No, not really"},
        
    ], indent=4))

# messages.append({"role": "assistant", "content":assistant_msg})

# user_message = input(">")
# messages.append({"role": "user", "content":user_message})

# messages_to_json = [x for x in messages]
# messages_to_json.append({"role": "system", "content": "Generate a json string with the key name and the legal name of the user as a value. If name not given yet, put null a value"})


# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-0613",
#     messages=messages_to_json
# )






exit()




def converse():
    null_object = Erc20AIResponse(name=None, symbol=None, owner=None, premint=None, mintable=None, burnable=None, pausable=None).json()

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


def validate_input(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        # messages=[
        # #    {"role": "system", "content": "I want to develop and ERC20 smart contract with the name ASDFASDF"},
        # {"role": "user", "content": "I want to develop and ERC20 smart contract with the name ASDFASDF"},
        # {"role": "user", "content": "I want the symbol to be ASD"},
        # {"role": "system", "content": "Obtain missing information"}
        # ],
        messages = messages,
        functions=[
            {
            "name": "get_answer_for_user_query",
            "description": "Ask user for ERC20 parameters, unknown parameters should be null",
            "parameters": Erc20AIResponse.schema()
            }
        ],
        function_call={"name": "get_answer_for_user_query"}
    )
    output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
    return output


if __name__ == "__main__":
    input_data = validate_input()
    print(input_data)
