# app/files/files.py
# Encrypted file storage

import os
from cryptography.fernet import Fernet
from app.blockchain.blockchain import Blockchain

FILES_DIR = "app/data/encrypted_files"
KEYS_DIR = "app/data/file_keys"

os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)


def generate_file_key(username):
    key_path = f"{KEYS_DIR}/{username}.key"

    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()

    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)

    return key


def encrypt_file(username, input_path):
    key = generate_file_key(username)
    fernet = Fernet(key)

    with open(input_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    filename = os.path.basename(input_path)
    output_path = f"{FILES_DIR}/{filename}.enc"

    with open(output_path, "wb") as f:
        f.write(encrypted)

    bc = Blockchain()
    bc.add_block([f"File encrypted by {username}: {filename}"])
    bc.save()

    return output_path


def decrypt_file(username, encrypted_path, output_path):
    key_path = f"{KEYS_DIR}/{username}.key"
    if not os.path.exists(key_path):
        raise ValueError("No key for user")

    with open(key_path, "rb") as f:
        key = f.read()

    fernet = Fernet(key)

    with open(encrypted_path, "rb") as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)

    with open(output_path, "wb") as f:
        f.write(decrypted)

    bc = Blockchain()
    bc.add_block([f"File decrypted by {username}"])
    bc.save()
