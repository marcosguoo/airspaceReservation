import random
import csv
import os
import time
from web3 import Web3

last_tx_hash = None

alchemy_endpoint = "https://eth-sepolia.g.alchemy.com/v2/f5CCM-LCyz4LDgyXg_V6Ihw6MPaBGxvl"
w3 = Web3(Web3.HTTPProvider(alchemy_endpoint))

contract_address = "0xcBdA1230141F56E6f7c3d7DA5CCf6A899edFbD2e"
owner_address = "0x8d3c36D37914691405F97C404B45d3FBB2126DAb"
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"winner","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"AuctionEnded","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"bidder","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"BidPlaced","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"clearer","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyClear","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"bids","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"emergencyClear","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endAuction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"highestBid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"highestBidder","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"placeBid","outputs":[],"stateMutability":"payable","type":"function"}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

owner_private_key = "c4133c6262e78b9cc61bce9972c9c256a640cb5d9e205fb3e91f1bd395000324"

private_keys = ["84b4091e15267b50f6645d44bb96b4bc3179377daa2a8808b224d9f579be1cf1", "0ed7b2db696a63d09cfc3f1372d18b7edb019ce61a90907b2ebaba7b9d209ee6", "e0023eb49080755858a869113960ff7077c814201a2bc44ea5579686e27841ea", "873027b1d6b90ba91c01056abd2a344d2120a12eefd300adae90bb64817e263c", "ced74225be9e26fed49fd7384a21677b4a6217d479c2987e46df3f9494677a6f"]

tx_hashes = []
estimated_fees = []
actual_fees = []

def place_random_bid(private_key, writer):
    account = w3.eth.account.from_key(private_key)
    account_address = account.address
    bid_amount = random.randint(500, 1000)
    current_gas_price = w3.eth.gas_price

    transaction = contract.functions.placeBid().build_transaction({
        'from': account_address,
        'value': bid_amount,
        'gasPrice': 2000000000,
        'nonce': w3.eth.get_transaction_count(account_address),
    })

    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction).hex()

    writer.writerow([account_address, bid_amount, tx_hash, current_gas_price, "Bid Attempted"])

    print(f"Bid attempted by {account_address}. Bid amount: {bid_amount} wei. Transaction hash: {tx_hash}. Gas price: {current_gas_price}")

    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
        writer.writerow([account_address, bid_amount, tx_hash, current_gas_price, "Bid Successful"])
        print(f"Bid successful by {account_address}. Transaction hash: {tx_hash}")
    except Exception as e:
        writer.writerow([account_address, bid_amount, tx_hash, current_gas_price, "Bid Failed"])
        print(f"Bid failed by {account_address}. Transaction hash: {tx_hash}. Error: {e}")

    print(f"Bid placed by {account_address}. Bid amount: {bid_amount} wei. Transaction hash: {tx_hash}. Gas price: {current_gas_price}")

def end_auction(writer):
    account = w3.eth.account.from_key(owner_private_key)

    for tx_hash in tx_hashes:
        w3.eth.wait_for_transaction_receipt(tx_hash)

    current_gas_price = w3.eth.gas_price * 1.1

    transaction = contract.functions.endAuction().build_transaction({
        'from': owner_address,
        'gasPrice': int(current_gas_price),
        'nonce': w3.eth.get_transaction_count(owner_address, 'pending'),
    })

    estimated_gas = w3.eth.estimate_gas(transaction)
    transaction['gas'] = int(estimated_gas * 1.2)

    signed_transaction = w3.eth.account.sign_transaction(transaction, owner_private_key)
    try:
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction).hex()
        print(f"Auction ended by the owner. Transaction hash: {tx_hash}. Gas price: {current_gas_price}")
    except ValueError as e:
        print(f"Failed to end auction: {e}")

    final_highest_bidder = contract.functions.highestBidder().call()
    final_highest_bid = contract.functions.highestBid().call()
    print(f"Final Highest Bidder: {final_highest_bidder}")
    print(f"Final Highest Bid: {final_highest_bid}")
    writer.writerow(['', '', '', '', '', final_highest_bidder, final_highest_bid])

def get_actual_gas_fee(w3, tx_hash):
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        gas_used = receipt.gasUsed
        effective_gas_price = receipt.effectiveGasPrice
        actual_gas_fee = gas_used * effective_gas_price
        return actual_gas_fee
    except Exception as e:
        print(f"Error fetching receipt for {tx_hash}: {e}")
        return None

def update_actual_gas_fee(tx_hash, index):
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    actual_gas_fee = receipt['gasUsed'] * receipt['effectiveGasPrice']

    with open('bidding_results.csv', mode='r+', newline='') as file:
        rows = list(csv.reader(file))
        rows[index + 1][-1] = actual_gas_fee
        file.seek(0)
        csv.writer(file).writerows(rows)

if __name__ == "__main__":
    csv_file_path = 'bidding_results.csv'
    write_headers = not os.path.exists(csv_file_path) or os.stat(csv_file_path).st_size == 0

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if write_headers:
            writer.writerow(['Sender', 'Bid Amount', 'Transaction Hash', 'Gas Price', 'Estimated Full Gas Fee', 'Actual Gas Fee'])

    for private_key in private_keys:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            place_random_bid(private_key, writer)

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        end_auction(writer)