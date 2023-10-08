import requests
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import sys


url = "http://127.0.0.1:8080/converse/choose-contract"

class ContractType(Enum):
    Erc20 = 'erc20'
    TimeLock = 'time-lock'
    Unsupported = 'unsupported'

class ContractTypeAIResponse(BaseModel):
    contractType: Optional[ContractType] = None

contract_type_schema = ContractTypeAIResponse.model_json_schema()
contract_type_null_object = ContractTypeAIResponse().model_dump_json()


if sys.argv[1] == "erc20":
    messages = [
        {"role": "system", "content": f"""
            You are a friendly assistant that needs to fill the json {contract_type_null_object}.
            The information should be given by the user.
            You should help the user decide what kind of smart contract he should use depending on his needs.
            If the user decides and confirms the contract and its an ERC20 you should set 'erc20' to the json.
            If the user decides and confirms the contract and its a Time-Lock contract you should set 'time-lock' to the json.
            The rest of the contracts are not supported at the moment.
            If the user needs any other contract you should add 'unsupported' to the json.
            Keep the conversation about the decision of the smart contract type.
        """},
        {"role": "assistant", "content": "How can I assist you today?"},
        {"role": "user", "content": "Can you tell me a joke?"},
        {"role": "assistant", "content": "Of course! Here's a joke for you: \n\nWhy don't scientists trust atoms? \n\nBecause they make up everything! \n\nNow, let's get back to your question. How can I assist you with your smart contract needs?"},
        {"role": "user", "content": "I want to create do a fundraising and keep track of how much each party has contributed to the fund raising."},
        {"role": "assistant", "content": "For fundraising and tracking contributions, you might consider using an ERC20 token contract. ERC20 is a widely used standard for creating fungible tokens on the Ethereum blockchain. It allows you to keep track of token balances for different parties and ensures compatibility with various wallets and exchanges. \n\nWith an ERC20 token contract, you can create tokens that represent the contributions made by each party. This would enable you to easily keep track of how much each party has contributed to the fundraising effort. \n\nDoes using an ERC20 token contract sound like it would meet your needs?"},
        
        # {"role": "user", "content": "No, I don't want an ERC20"},
        # {"role": "assistant", "content": "Understood. If an ERC20 token contract doesn't meet your needs, could you please provide more details about the type of smart contract you have in mind for your fundraising? This will help me suggest a more suitable contract for your specific requirements."},
        # {"role": "user", "content": "What is an ERC20 contract?"},
    ]
elif sys.argv[1] == "time-lock":
    messages = [
        {"role": "system", "content": f"""
            You are a friendly assistant that needs to fill the json {contract_type_null_object}.
            The information should be given by the user.
            You should help the user decide what kind of smart contract he should use depending on his needs.
            If the user decides and confirms the contract and its an ERC20 you should set 'erc20' to the json.
            If the user decides and confirms the contract and its a Time-Lock contract you should set 'time-lock' to the json.
            The rest of the contracts are not supported at the moment.
            If the user needs any other contract you should add 'unsupported' to the json.
            Keep the conversation about the decision of the smart contract type.
        """},
        {"role": "assistant", "content": "Hello! I'm here to help you decide on the type of smart contract you need. Can you please provide me with some information about your requirements? Specifically, what do you intend to use the smart contract for?"},
        {"role": "user", "content": "I would like to create a contract that will hold my childs funds until he reaches a certain age"},
        {"role": "assistant", "content": "That sounds like you need a time-lock contract. A time-lock contract can hold funds until a specific condition is met, such as a certain age being reached. This can be useful for situations like managing funds for minors until they come of age.\n\nWould you like to proceed with a time-lock contract?"},
        {"role": "user", "content": "Yes, lets do a time lock contract"},
        # {"role": "assistant", "content": "For fundraising and tracking contributions, you might consider using an ERC20 token contract. ERC20 is a widely used standard for creating fungible tokens on the Ethereum blockchain. It allows you to keep track of token balances for different parties and ensures compatibility with various wallets and exchanges. \n\nWith an ERC20 token contract, you can create tokens that represent the contributions made by each party. This would enable you to easily keep track of how much each party has contributed to the fundraising effort. \n\nDoes using an ERC20 token contract sound like it would meet your needs?"},
        # {"role": "user", "content": "No, I don't want an ERC20"},
        # {"role": "assistant", "content": "Understood. If an ERC20 token contract doesn't meet your needs, could you please provide more details about the type of smart contract you have in mind for your fundraising? This will help me suggest a more suitable contract for your specific requirements."},
        # {"role": "user", "content": "What is an ERC20 contract?"},
    ]
elif sys.argv[1] == "nft":
    messages = [
        {"role": "system", "content": f"""
            You are a friendly assistant that needs to fill the json {contract_type_null_object}.
            The information should be given by the user.
            You should help the user decide what kind of smart contract he should use depending on his needs.
            If the user decides and confirms the contract and its an ERC20 you should set 'erc20' to the json.
            If the user decides and confirms the contract and its a Time-Lock contract you should set 'time-lock' to the json.
            The rest of the contracts are not supported at the moment.
            If the user needs any other contract you should add 'unsupported' to the json.
            Keep the conversation about the decision of the smart contract type.
        """},
        {"role": "assistant", "content": "Hello! I'm here to help you decide on the type of smart contract you need. Can you please provide me with some information about your requirements? Specifically, what do you intend to use the smart contract for?"},
        {"role": "user", "content": "I would like to create an NFT"},
        {"role": "assistant", "content": "That's great! NFTs (Non-Fungible Tokens) are a popular use case in the blockchain space. To create an NFT, you have a few options. One way is to use the ERC721 standard, which is specifically designed for NFTs. Another option is to use the newer ERC1155 standard, which supports both fungible and non-fungible tokens.\n\nWould you like to create your NFT using the ERC721 standard or the ERC1155 standard?"},
        {"role": "user", "content": "What is the difference?"},
        {"role": "assistant", "content": "The main difference between the ERC721 and ERC1155 standards lies in their token structure and functionality.\n\nERC721: The ERC721 standard is specifically designed for non-fungible tokens. It allows you to create unique tokens that are distinct from each other. Each token within an ERC721 contract has a unique identifier, and they cannot be divided or replaced with another token. This makes ERC721 ideal for creating one-of-a-kind assets like collectibles, art pieces, or unique digital items.\n\nERC1155: The ERC1155 standard, on the other hand, is a more versatile standard that supports both fungible and non-fungible tokens. With ERC1155, you can create both unique and identical tokens within the same contract. This allows for greater flexibility, as you can create both NFTs and multiple instances of a fungible token (like a currency or in-game item) within the same contract. ERC1155 can be a good choice if you're planning to create a mixture of NFTs and Fungible tokens within your project.\n\nUltimately, the choice between ERC721 and ERC1155 depends on your specific requirements and the nature of the NFTs you want to create. Let me know which standard you prefer, and I can assist you further with the type of contract you need."},
        {"role": "user", "content": "I see, I think I will need an ERC721 then"},
        # {"role": "assistant", "content": "Understood. If an ERC20 token contract doesn't meet your needs, could you please provide more details about the type of smart contract you have in mind for your fundraising? This will help me suggest a more suitable contract for your specific requirements."},
        # {"role": "user", "content": "What is an ERC20 contract?"},
    ]


resp = requests.post(url=url, json={"messages": messages})

print(resp.json())
