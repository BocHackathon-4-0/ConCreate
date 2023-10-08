from flask import Flask, request, jsonify, render_template
import openai
import json
from typing import List, Optional
from pydantic import BaseModel
from solcx import compile_source, compile_standard, install_solc
from datetime import datetime
from enum import Enum
from flask_cors import CORS
from llm.Erc20 import erc20_null_object, validate_erc20_input
from llm.Lock import lock_null_object, validate_lock_input
from llm.ContractType import contract_type_null_object, validate_contract_type_input
from llm.ContractGen import generate_code
import os
from web3 import Web3


# Set up your API key
openai.api_key = os.environ.get("OPENAI_TOKEN", "")

install_solc('0.8.20')

app = Flask(__name__)
CORS(app)


@app.route("/")
def index_ep():
    return "hello world"


@app.route("/converse/code-gen", methods=["POST"])
def code_gen_converse():
    messages = request.json.get("messages", [])
    return generate_code(messages)


@app.route("/converse/choose-contract", methods=["POST"])
def choose_contract_converse():
    messages = request.json.get("messages", [])
    messages = [{"role": "system", "content": f"""
                    You are a friendly assistant that needs to fill the json {contract_type_null_object}.
                    The information should be given by the user.
                    You should help the user decide what kind of smart contract he should use depending on his needs.
                    If the user decides the contract and its an ERC20 you should set 'erc20' to the json.
                    If the user decides the contract and its a Time-Lock contract you should set 'time-lock' to the json.
                    If the user decides to generate a custom contract you should set 'custom' to the json.
                    The rest of decides the contracts are not supported at the moment.
                    If the user needs any other contract you should add 'unsupported' to the json.
                """}] + list(filter(lambda x: x.get("role").lower() != "system", messages))
    value_success, data = validate_contract_type_input(messages)

    if not value_success:
        return jsonify(data)
    
    user_input = data

    if len(user_input) > 0 and None not in [v for k, v in user_input.items()]:
        return jsonify(user_input)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    assistant_msg = response["choices"][0]["message"]
    return assistant_msg


@app.route("/converse/erc20", methods=["POST"])
def erc20_converse():
    messages = request.json.get("messages", [])
    messages = [{"role": "system", "content": f"""
                    You are a friendly assistant that needs to fill the json {erc20_null_object}.
                    The information should be given by the user.
                    The information is about an ERC20 smart contract.
                """}] + list(filter(lambda x: x.get("role").lower() != "system", messages))
    value_success, data = validate_erc20_input(messages)

    if not value_success:
        return jsonify(data)
    
    user_input = data

    print(user_input)
    
    if len(user_input) > 0 and None not in [v for _, v in user_input.items()]:

        smart_contract = render_template("erc20.sol", **user_input)
        compiled_sol = compile_source(smart_contract, output_values=["abi", "bin"], solc_version="0.8.20", import_remappings=["@openzeppelin=./openzeppelin-contracts-5.0.0"], )
        return jsonify({
            "bin": compiled_sol.get("<stdin>:MyToken", {}).get("bin", ""),
            "src": smart_contract
        })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    assistant_msg = response["choices"][0]["message"]
    return assistant_msg


@app.route("/converse/lock", methods=["POST"])
def lock_converse():
    messages = request.json.get("messages", [])
    messages = [{"role": "system", "content": f"""
                    You are a friendly assistant that needs to fill the json {lock_null_object}.
                    The information should be given by the user.
                    The information is about an time-lock smart contract.
                """}] + list(filter(lambda x: x.get("role").lower() != "system", messages))
    value_success, data = validate_lock_input(messages)
    if not value_success:
        # return jsonify({"role": "assistant", "content": data})
        return jsonify(data)
    
    user_input = data

    if len(user_input) > 0 and None not in [v for k, v in user_input.items()]:
        smart_contract = render_template("lock.sol", **user_input)
        compiled_sol = compile_source(smart_contract, output_values=["abi", "bin"], solc_version="0.8.20", import_remappings=["@openzeppelin=./openzeppelin-contracts-5.0.0"], )
        return jsonify({
            "bin": compiled_sol.get("<stdin>:Lock", {}).get("bin", ""),
            "src": smart_contract
        })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    assistant_msg = response["choices"][0]["message"]
    return assistant_msg


@app.route("/test")
def test_ep():
    user_input = {'name': 'KOKOSPOROSICOIN', 'symbol': 'KPC', 'owner': '0xF80214FD406294c2A44ef7A1D548793e12Ae8E5c', 'premint': 100, 'mintable': False, 'burnable': True, 'pausable': False}
    smart_contract = render_template("erc20.sol", **user_input)
    compiled_sol = compile_source(smart_contract, output_values=["abi", "bin"], solc_version="0.8.20", import_remappings=["@openzeppelin=./openzeppelin-contracts-5.0.0"], )
    return jsonify({
        "bin": compiled_sol.get("<stdin>:MyToken", {}).get("bin", ""),
        "src": smart_contract
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
