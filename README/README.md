📄 README.md — Setup & Usage

# CryptoVault – Secure Cryptographic System

CryptoVault is a secure multi-module system implementing:
- Strong user authentication with TOTP
- Secure encrypted messaging
- File encryption and decryption
- Blockchain-based audit ledger

The project is implemented using FastAPI and cryptographic primitives built from scratch.

---
## Requirements
- Python 3.10+
- pip
- Virtual environment (recommended)

---
## Installation
```bash
git clone <repository>
cd crypto-final
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Running the Application
uvicorn app.main:app --reload

Open your browser and go to:
http://127.0.0.1:8000