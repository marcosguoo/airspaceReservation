import time
import csv
from web3 import Web3

# Connect to Alchemy
alchemy_url = 'https://eth-mainnet.g.alchemy.com/v2/iFI1iCMW5h656qZ-jr-zqaRjnMh5DCbR'
w3 = Web3(Web3.HTTPProvider(alchemy_url))

def fetch_block_data(block_number):
    block = w3.eth.get_block(block_number, full_transactions=True)
    return block

def analyze_block(block):
    gas_limit = block.gasLimit
    block_time = block.timestamp
    transaction_count = len(block.transactions)
    block_size = block.size
    gas_used = block.gasUsed
    network_utilization = gas_used / gas_limit
    total_gas_price = 0
    failed_transaction_count = 0
    transaction_hashes = []

    for tx in block.transactions:
        total_gas_price += tx.gasPrice
        transaction_hashes.append(tx.hash.hex())
        # Check if transaction receipt status is 0 (failed)
        receipt = w3.eth.get_transaction_receipt(tx.hash)
        if receipt.status == 0:
            failed_transaction_count += 1

    average_gas_price = total_gas_price // transaction_count if transaction_count > 0 else 0
    total_transaction_fees = gas_used * average_gas_price

    return {
        'block_number': block.number,
        'gas_limit': gas_limit,
        'block_time': block_time,
        'transaction_count': transaction_count,
        'block_size': block_size,
        'network_utilization': network_utilization,
        'average_gas_price': average_gas_price,
        'total_transaction_fees': total_transaction_fees,
        'number_of_uncles': len(block.uncles),
        'difficulty': block.difficulty,
        'total_difficulty': block.totalDifficulty,
        'transaction_hashes': transaction_hashes,
        'failed_transaction_count': failed_transaction_count
    }

def write_to_csv(data, filename="blockchain_data.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

def monitor_network():

    block_number = w3.eth.block_number
    block = fetch_block_data(block_number)
    analysis = analyze_block(block)
    write_to_csv(analysis)
    print(f"Data for block {block_number} saved.")

# Start monitoring
monitor_network()
