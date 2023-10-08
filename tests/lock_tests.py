import requests
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


url = "http://127.0.0.1:8080/converse/lock"

class LockAIResponse(BaseModel):
    owner: Optional[str]
    unlockTime: Optional[str]

lock_schema = LockAIResponse.model_json_schema()
lock_null_object = LockAIResponse(owner=None, unlockTime=None).model_dump_json()


messages = [
    {"role": "system", "content": f"""You are a friendly assistant that needs to fill the json {lock_null_object}. The information should be given by the user. The information is about a time-lock smart contract."""},
    {"role": "assistant", "content": "Please provide the owner's address and the unlock time for the time-lock smart contract."},
    {"role": "user", "content": "The owner should be Alex"},
    {"role": "assistant", "content": "Thank you for providing the owner's name. Could you also please provide the owner's Ethereum address?"},
    {"role": "user", "content": "0xF80214FD406294c2A44ef7A1D548793e12Ae8E5c"},
    {"role": "assistant", "content": "Thank you for providing the owner's Ethereum address. Now, could you please provide the unlock time for the time-lock smart contract?"},
    {"role": "user", "content": "10th of december 2023"},
    {"role": "assistant", "content": "To avoid inconsistencies with date formats please use the date format YYYY-MM-DD HH:MM for the unlock time"},
    {"role": "user", "content": "2023-11-03 11:30"},
]

resp = requests.post(url=url, json={"messages": messages})

print(resp.json())
