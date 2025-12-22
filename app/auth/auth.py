# app/auth/auth.py
# User authentication

import json
import os
from argon2 import PasswordHasher
from app.auth.totp import generate_totp_secret, verify_totp
from app.blockchain.blockchain import Blockchain

ph = PasswordHasher()
USERS_FILE = "app/data/users.json"
SESSIONS_FILE = "app/data/sessions.json"


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def register_user(username, password):
    users = load_json(USERS_FILE)
    if username in users:
        raise ValueError("User already exists")

    password_hash = ph.hash(password)
    totp_secret = generate_totp_secret()

    users[username] = {
        "password": password_hash,
        "totp_secret": totp_secret
    }

    save_json(USERS_FILE, users)

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
    except:
        return False

    if not verify_totp(users[username]["totp_secret"], totp_code):
        return False

    sessions = load_json(SESSIONS_FILE)
    sessions[username] = True
    save_json(SESSIONS_FILE, sessions)

    bc = Blockchain()
    bc.add_block([f"User {username} logged in"])
    bc.save()

    return True
