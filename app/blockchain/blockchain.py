import time, json
from app.core.sha256 import sha256
from app.core.merkle import merkle_root

CHAIN = "app/data/blockchain.json"

def load_chain():
    try:
        with open(CHAIN) as f:
            return json.load(f)
    except:
        return []

def save_chain(chain):
    with open(CHAIN, "w") as f:
        json.dump(chain, f, indent=2)

def log_event(event):
    chain = load_chain()
    prev = chain[-1]["hash"] if chain else "0"*64

    block = {
        "index": len(chain),
        "timestamp": int(time.time()),
        "event": event,
        "prev_hash": prev
    }

    block["hash"] = sha256(str(block).encode())
    chain.append(block)
    save_chain(chain)
