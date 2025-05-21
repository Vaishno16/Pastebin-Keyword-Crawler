"""Pastebin Keyword Crawler (Crypto / t.me).ipynb
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime

ARCHIVE_URL = "https://pastebin.com/archive"
RAW_URL = "https://pastebin.com/raw/{}"
KEYWORDS = [
    "crypto", "bitcoin", "ethereum", "blockchain", "t.me", "wallet", "token",
    "airdrop", "ICO", "DeFi", "NFT", "altcoin", "smart contract", "staking",
    "DAO", "mining", "hashrate", "DEX", "crypto exchange", "cold wallet",
    "hot wallet", "ledger", "metamask", "gas fees", "yield farming", "layer 2",
    "crypto pump", "crypto dump", "satoshi", "cryptocurrency", "binance",
    "coinbase", "solana", "polkadot", "ripple", "cardano", "chainlink",
    "litecoin", "dogecoin", "shiba inu", "terra", "avalanche", "uniswap",
    "pancakeswap", "decentralized", "tokenomics", "validator", "fork",
    "mainnet", "testnet", "private key", "public key", "exchange", "fiat",
    "cold storage", "hot storage", "gas limit", "gas price", "hash",
    "consensus", "proof of work", "proof of stake", "staking rewards",
    "airdrops", "whitelist", "IDO", "IEO", "layer 1", "cross-chain",
    "oracle", "cryptography", "block reward", "coin burn", "liquidity pool",
    "impermanent loss", "flash loan", "rug pull", "DAO hack", "token swap",
    "moonshot", "rekt", "hodl", "fomo", "fud", "block explorer", "node",
    "dApp", "yield aggregator", "staking pool", "token launch", "market cap",
    "volume", "burn address", "token lock", "vesting", "whitepaper",
    "airdropped tokens", "cryptojacking", "smart contract audit", "multisig",
    "gas token", "wrapped token", "cryptopunk", "decentralized finance",
    "cross-chain bridge", "block time", "sharding", "liquidity mining",
    "staking contract", "token sale", "token minting"
]

OUTPUT_FILE = "keyword_matches.jsonl"
HEADERS = {"User-Agent": "Mozilla/5.0"}
checked_ids = set()
MAX_RETRIES = 3

def get_recent_pastes(limit=100):
    try:
        res = requests.get(ARCHIVE_URL, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select("table.maintable a[href^='/']")
        paste_ids = list({link['href'].split('/')[-1] for link in links})
        return paste_ids[:limit]
    except Exception as e:
        print(f"Error fetching archive: {e}")
        return []

def get_paste_content(paste_id):
    try:
        res = requests.get(RAW_URL.format(paste_id), headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return res.text
    except Exception as e:
        print(f"Error fetching paste {paste_id}: {e}")
    return None

def find_keywords(text):
    return [k for k in KEYWORDS if k.lower() in text.lower()]

def save_result(paste_id, keywords):
    data = {
        "source": "pastebin",
        "context": f"Found crypto content in paste {paste_id}",
        "paste_id": paste_id,
        "url": RAW_URL.format(paste_id),
        "discovered_at": datetime.utcnow().isoformat() + "Z",
        "keywords_found": keywords,
        "status": "pending"
    }
    with open(OUTPUT_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    print(f"Match found: {paste_id} -> {keywords}")

def monitor():
    retries = 0
    while retries < MAX_RETRIES:
        found_in_cycle = False
        recent = get_recent_pastes()
        new_pastes = [pid for pid in recent if pid not in checked_ids]

        for pid in new_pastes:
            checked_ids.add(pid)
            print(f"Checking {pid}...")
            content = get_paste_content(pid)
            if content:
                matches = find_keywords(content)
                if matches:
                    save_result(pid, matches)
                    found_in_cycle = True
            time.sleep(2)  # be polite to server

        if found_in_cycle:
            retries = 0  # reset retries if we found matches
            print("Matches found this cycle, continuing monitoring...")
        else:
            retries += 1
            print(f"No matches this cycle. Retry {retries}/{MAX_RETRIES}. Waiting 60 seconds before next try...")
            time.sleep(10)

    print("Reached max retries with no matches. Stopping monitor.")

if __name__ == "__main__":
    monitor()