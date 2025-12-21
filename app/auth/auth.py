import json, secrets, hmac, time
from argon2 import PasswordHasher
from app.core.sha256 import sha256

ph = PasswordHasher()

USERS = "app/data/users.json"
SESSIONS = "app/data/sessions.json"

def load(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def register(username, password, totp_secret):
    users = load(USERS)
    if username in users:
        raise ValueError("User exists")

    users[username] = {
        "password": ph.hash(password),
        "totp": totp_secret
    }
    save(USERS, users)

def login(username, password):
    users = load(USERS)
    if username not in users:
        return None

    try:
        ph.verify(users[username]["password"], password)
    except:
        return None

    token = hmac.new(
        secrets.token_bytes(32),
        f"{username}{time.time()}".encode(),
        "sha256"
    ).hexdigest()

    sessions = load(SESSIONS)
    sessions[token] = username
    save(SESSIONS, sessions)
    return token
