import requests
from typing import List, Optional
from pydantic import BaseModel


url = "http://127.0.0.1:8080/converse/erc20"

class Erc20AIResponse(BaseModel):
    name: Optional[str]
    symbol: Optional[str]
    owner: Optional[str]
    premint: Optional[int]
    mintable: Optional[bool]
    burnable: Optional[bool]
    pausable: Optional[bool]
    # votes: Optional[bool]

erc20_schema = Erc20AIResponse.model_json_schema()
erc20_null_object = Erc20AIResponse(name=None, symbol=None, owner=None, premint=None, mintable=None, burnable=None, pausable=None).model_dump_json()


messages = [
    # {"role": "system", "content": f"You are a friendly assistant that asks the user for information to fill the json {erc20_null_object} about an ERC20 deployment"},
    {"role": "system", "content": f"""You are a friendly assistant that needs to fill the json {erc20_null_object}. The information should be given by the user. The information is about an ERC20 smart contract."""},
    {"role": "assistant", "content": "What is the name of the ERC20 smart contract?"},
    {"role": "user", "content": "My contract name should be KOKOSPOROSICOIN"},
    # {"role": "assistant", "content": "What is the symbol for the ERC20 smart contract?"},
    # {"role": "user", "content": "My contract name should be KPC"},
    # {"role": "assistant", "content": "Who will be the owner of the ERC20 smart contract?"},
    # {"role": "user", "content": "Why do you need this information?"},
    # {"role": "assistant", "content": "The owner of the ERC20 smart contract is the address that will have special administrative privileges, such as the ability to change contract parameters, mint new tokens, or perform other administrative functions."},
    # {"role": "user", "content": "Ah, I see, the contract owner will be me"},
    # {"role": "assistant", "content": "What is your wallet address?"},
    # {"role": "user", "content": "The address is Faneromenis 23, Nicosia, Cyprus"},
    # {"role": "assistant", "content": "I apologize for the misunderstanding. The owner of the ERC20 smart contract should be a wallet address, which is typically represented as a string of alphanumeric characters. Could you please provide a valid wallet address as the owner of the contract?"},
    # {"role": "user", "content": "0xF80214FD406294c2A44ef7A1D548793e12Ae8E5c"},
    # {"role": "assistant", "content": "How many tokens would you like to pre-mint for the ERC20 smart contract?"},
    # {"role": "user", "content": "100"},
    # {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be mintable?"},
    # {"role": "user", "content": "Yes please"},
    # {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be burnable?"},
    # {"role": "user", "content": "No"},
    # {"role": "assistant", "content": "Would you like the ERC20 smart contract tokens to be pausable?"},
    # {"role": "user", "content": "No, not really"},
    
]

resp = requests.post(url=url, json={"messages": messages})

print(resp.json())
# print(resp.text)
