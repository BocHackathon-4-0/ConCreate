import requests
from typing import List, Optional
from pydantic import BaseModel


url = "http://127.0.0.1:8080/converse/code-gen"

class CodeGenAIResponse(BaseModel):
    code: Optional[str] = None


contract_type_schema = CodeGenAIResponse.model_json_schema()
contract_type_null_object = CodeGenAIResponse(name=None, symbol=None, owner=None, premint=None, mintable=None, burnable=None, pausable=None).model_dump_json()


messages = [
    {"role": "user", "content": """
         I would like to have a smart contract that has a list of addresses that are allowed to vote 'for' or 'against'.
         Each address can vote once.
         If more than half of the addresses voted 'for' the result is locked.
         If more than half of the addresses voted 'against' the result is locked.
         The addresses that are allowed to vote are 0x83589b6CA59beE1e4D74e9bAA385de640602b0Ff, 0x0dD3dbbAef874d4Bbf1197Ca2ff0059AC15cD8FD and 0x53FF5656b2fc048536f7de41ae1C39EbE2E26599  
    """},
]

resp = requests.post(url=url, json={"messages": messages})

data = resp.json()
# print(resp.text)

print(data)

for k, v in data.items():
    print(k)
    print(v)
