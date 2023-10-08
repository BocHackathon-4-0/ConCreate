import openai
import json
from typing import List, Optional
from pydantic import BaseModel
import tempfile
import subprocess
import os


# Set up your API key
openai.api_key = os.environ.get("OPENAI_TOKEN", "")




class CodeGenAIResponse(BaseModel):
    code: Optional[str] = None


schema = CodeGenAIResponse.model_json_schema()
null_object = CodeGenAIResponse(name=None, symbol=None, owner=None, premint=None, mintable=None, burnable=None, pausable=None).model_dump_json()



response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "system", "content": "Write code a solidity smart contract that implements what the user describes"},
    # {"role": "user", "content": "I want to develop and ERC20 smart contract with the name ASDFASDF"},
        {"role": "user", "content": """
         I would like to have a smart contract that has a list of addresses that are allowed to vote 'for' or 'against'.
         Each address can vote once.
         If more than half of the addresses voted 'for' the result is locked.
         If more than half of the addresses voted 'against' the result is locked.
         The addresses that are allowed to vote are 0x83589b6CA59beE1e4D74e9bAA385de640602b0Ff, 0x0dD3dbbAef874d4Bbf1197Ca2ff0059AC15cD8FD and 0x53FF5656b2fc048536f7de41ae1C39EbE2E26599  
        """},
        #  Introduce an integer overflow so I can detect it using automated analysis.
        # {"role": "system", "content": "Obtain missing information"}
    ],
    functions=[
        {
        "name": "get_answer_for_user_query",
        "description": "Generate the solidity code the user asked for",
        "parameters": CodeGenAIResponse.model_json_schema()
        }
    ],
    function_call={"name": "get_answer_for_user_query"}
)

try:
    code = json.loads(response.choices[0]["message"]["function_call"]["arguments"])["code"]
except:
    broken_json = response.choices[0]["message"]["function_call"]["arguments"]
    pragma_start = broken_json.find("pragma")
    last_quote = broken_json.rfind('"')
    code = broken_json[pragma_start:last_quote]
print(code)

tmp = tempfile.NamedTemporaryFile(delete=False)
tmp.write(code)
tmp.close()

result = subprocess.check_output(['myth', 'analyze', tmp.name])

os.unlink(tmp.name)

if "The analysis was completed successfully. No issues were detected." in result:
    status = "clean"

else:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": f"""
                Explain the following mythril analysis result.
                {result}
                """},
        ],
    )
    print(response)



exit()


result = """
==== Integer Arithmetic Bugs ====
SWC ID: 101
Severity: High
Contract: VulnerableToken
Function name: burn(uint256)
PC address: 369
Estimated Gas Usage: 7040 - 27515
The arithmetic operator can underflow.
It is possible to cause an integer overflow or underflow in the arithmetic operation. 
--------------------
In file: test1/VulnerableToken.sol:24

balances[msg.sender] -= val

--------------------
Initial State:

Account: [CREATOR], balance: 0x0, nonce:0, storage:{}
Account: [ATTACKER], balance: 0x0, nonce:0, storage:{}

Transaction Sequence:

Caller: [CREATOR], calldata: , decoded_data: , value: 0x0
Caller: [CREATOR], function: burn(uint256), txdata: 0x42966c6800000000000000000000000000000000000000000000000001000000000f4241, decoded_data: (72057594038927937,), value: 0x0

==== Integer Arithmetic Bugs ====
SWC ID: 101
Severity: High
Contract: VulnerableToken
Function name: fund()
PC address: 728
Estimated Gas Usage: 7850 - 28655
The arithmetic operator can overflow.
It is possible to cause an integer overflow or underflow in the arithmetic operation. 
--------------------
In file: test1/VulnerableToken.sol:16

balances[msg.sender] += n

--------------------
Initial State:

Account: [CREATOR], balance: 0x54bc19b08b23f3a38, nonce:0, storage:{}
Account: [ATTACKER], balance: 0x0, nonce:0, storage:{}

Transaction Sequence:

Caller: [CREATOR], calldata: , decoded_data: , value: 0x0
Caller: [CREATOR], function: burn(uint256), txdata: 0x42966c6800000000000000000000000000000000000000000000000000000000000f4241, decoded_data: (1000001,), value: 0x0
Caller: [CREATOR], function: fund(), txdata: 0xb60d4288, value: 0x1

==== Integer Arithmetic Bugs ====
SWC ID: 101
Severity: High
Contract: VulnerableToken
Function name: fund()
PC address: 908
Estimated Gas Usage: 13772 - 54767
The arithmetic operator can overflow.
It is possible to cause an integer overflow or underflow in the arithmetic operation. 
--------------------
In file: test1/VulnerableToken.sol:18

balances[msg.sender] += n

--------------------
Initial State:

Account: [CREATOR], balance: 0x50000000000000001, nonce:0, storage:{}
Account: [ATTACKER], balance: 0x0, nonce:0, storage:{}

Transaction Sequence:

Caller: [CREATOR], calldata: , decoded_data: , value: 0x0
Caller: [CREATOR], function: burn(uint256), txdata: 0x42966c6800000000000000000000000000000000000000000000000000000000000f4242, decoded_data: (1000002,), value: 0x0
Caller: [CREATOR], function: fund(), txdata: 0xb60d4288, value: 0x1
"""

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "system", "content": f"""
            Explain the following mythril analysis result.
            {result}
            """},
    ],
)

print(response)




# output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])

# print(output)

# if __name__ == "__main__":
#     input_data = validate_input()
#     print(input_data)
