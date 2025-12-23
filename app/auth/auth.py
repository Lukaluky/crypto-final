# app/auth/auth.py
# User authentication

import json
import os
from argon2 import PasswordHasher

from app.auth.totp import generate_totp_secret, verify_totp
from app.blockchain.blockchain import Blockchain

ph = PasswordHasher()

# --- Paths ---
DATA_DIR = "app/data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def load_json(path):
    """
    Safe JSON loader:
    - returns {} if file does not exist
    - returns {} if file is empty or corrupted
    """
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def register_user(username, password):
    users = load_json(USERS_FILE)

    if username in users:
        # Явно возвращаем None вместо краша сервера
        return None

    password_hash = ph.hash(password)
    totp_secret = generate_totp_secret()

    users[username] = {
        "password": password_hash,
        "totp_secret": totp_secret
    }

    save_json(USERS_FILE, users)

    # Blockchain log
    bc = Blockchain()
    bc.add_block([f"User {username} registered"])
    bc.save()

    return totp_secret


def login_user(username, password, totp_code):
    users = load_json(USERS_FILE)

    if username not in users:
        return False

    try:
        ph.verify(users[username]["password"], password)
    except Exception:
        return False

    if not verify_totp(users[username]["totp_secret"], totp_code):
        return False

    sessions = load_json(SESSIONS_FILE)
    sessions[username] = True
    save_json(SESSIONS_FILE, sessions)

    # Blockchain log
    bc = Blockchain()
    bc.add_block([f"User {username} logged in"])
    bc.save()

    return True
