import json
import csv
import sqlite3
import bech32
import binascii
import traceback
import getpass
import argparse
import sys
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Spacemesh DB Reader")
    parser.add_argument("--rewards", "-r", action="store_true", help="Get Rewards for a Coinbase")
    parser.add_argument("--coinbase", "-c", type=str, help="Coinbase")
    parser.add_argument("--ouput-dir", "-o", type=str, help="Where the files will be output. Default is current directory", default="./")

    # Parse the command-line arguments
    args = parser.parse_args()
    return {
        "coinbase": args.coinbase,
        "rewards": args.rewards,
        "output": args.ouput_dir
    }

def bech32_to_hex(bech32_string):
    """Decode a bech32 encoded string into its hex representation."""
    hrp, words = bech32.bech32_decode(bech32_string)
    data = bech32.convertbits(words, frombits=5, tobits=8, pad=False)
    return bytes(data).hex()

def hex_to_bech32(hex_string):
    """Encode a hexadecimal string as a Bech32 string."""
    # Convert the hex string to bytes
    data = hex_string
    
    # Convert bytes to a list of integers
    byte_list = list(data)

    # Convert the byte list to words with 5-bit encoding
    words = bech32.convertbits(byte_list, frombits=8, tobits=5, pad=True)
    
    # Encode the words as Bech32 with the specified HRP
    bech32_string = bech32.bech32_encode("sm", words)
    
    return bech32_string

def output_csv(data, output_dir, name):
    if '.csv' not in name:
        name = name + '.csv'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f'{output_dir}/{name}', mode="w", newline="") as file:
        # Use newline="" to ensure correct line endings on different platforms
        writer = csv.writer(file)
        
        # Write the data to the CSV file
        writer.writerows(data)

def query_db(query_type, db_location, data):
    results = None
    try:
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        if query_type == 'rewards':
            query = f'select * from rewards where lower(hex(coinbase)) = "{data}"'

        cursor.execute(query)
        results = cursor.fetchall()
        
    
    except Exception as e:
        print(f'Error: {e}')
        traceback.print_exc()

    connection.close()
    return results

def get_rewards(args, config):
    coinbase = args["coinbase"]
    output = args["output"]

    if not coinbase:
        sys.exit("ERROR: No coinbase provided to query rewards")
    
    # We must convert the coinbase in order to query for it
    hex_coinbase = bech32_to_hex(coinbase)
    results = query_db('rewards', config["db_location"], hex_coinbase)
    
    csv_rewards = [["coinbase", "layer", "reward"]]
    for reward in results:
        csv_rewards.append([hex_to_bech32(reward[0]), reward[1], reward[2]/1000000000])

    output_csv(csv_rewards, output, f"rewards_{coinbase}.csv")

if __name__ == "__main__":
    args = parse_args()
    print(args)
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    if args['rewards']:
        get_rewards(args, config)

