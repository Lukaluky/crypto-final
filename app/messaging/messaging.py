# app/messaging/messaging.py
# Encrypted messaging using RSA

import json
import os
from app.core.rsa_math import generate_rsa_keys, encrypt, decrypt
from app.blockchain.blockchain import Blockchain

MESSAGES_FILE = "app/data/messages.json"
KEYS_FILE = "app/data/keys.json"


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# Generate RSA keys for user
def init_user_keys(username):
    keys = load_json(KEYS_FILE)

    if username in keys:
        return keys[username]

    public_key, private_key = generate_rsa_keys()
    keys[username] = {
        "public": list(public_key),
        "private": list(private_key)
    }

    save_json(KEYS_FILE, keys)
    return keys[username]


# Send encrypted message
def send_message(sender, receiver, message: str):
    keys = load_json(KEYS_FILE)
    messages = load_json(MESSAGES_FILE)

    if receiver not in keys:
        raise ValueError("Receiver has no keys")

    public_key = tuple(keys[receiver]["public"])

    encrypted = [encrypt(ord(c), public_key) for c in message]

    messages.setdefault(receiver, []).append({
        "from": sender,
        "cipher": encrypted
    })

    save_json(MESSAGES_FILE, messages)

    bc = Blockchain()
    bc.add_block([f"Message sent from {sender} to {receiver}"])
    bc.save()


# Read and decrypt messages
def read_messages(username):
    keys = load_json(KEYS_FILE)
    messages = load_json(MESSAGES_FILE)

    if username not in keys:
        raise ValueError("User has no keys")

    private_key = tuple(keys[username]["private"])

    decrypted_messages = []

    for msg in messages.get(username, []):
        text = "".join(chr(decrypt(c, private_key)) for c in msg["cipher"])
        decrypted_messages.append({
            "from": msg["from"],
            "message": text
        })

    return decrypted_messages
