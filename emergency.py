import random
import time
from web3 import Web3

alchemy_endpoint = "https://eth-sepolia.g.alchemy.com/v2/f5CCM-LCyz4LDgyXg_V6Ihw6MPaBGxvl"

w3 = Web3(Web3.HTTPProvider(alchemy_endpoint))

contract_address = "0xcBdA1230141F56E6f7c3d7DA5CCf6A899edFbD2e"
owner_address = "0x8d3c36D37914691405F97C404B45d3FBB2126DAb"
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"winner","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"AuctionEnded","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"bidder","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"BidPlaced","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"clearer","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyClear","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"bids","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"emergencyClear","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endAuction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"highestBid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"highestBidder","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"placeBid","outputs":[],"stateMutability":"payable","type":"function"}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

owner_private_key = "c4133c6262e78b9cc61bce9972c9c256a640cb5d9e205fb3e91f1bd395000324"

def call_emergency_clear():

    transaction = contract.functions.emergencyClear().build_transaction({
        'from': owner_address,
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(owner_address),
    })

    signed_transaction = w3.eth.account.sign_transaction(transaction, owner_private_key)

    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    print(f'Transaction sent. Transaction hash: {transaction_hash.hex()}')

tx_hash = call_emergency_clear()
print('Emergency!')