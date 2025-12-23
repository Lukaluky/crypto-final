
---

## ** architecture.md**

```markdown
# CryptoVault – System Architecture

CryptoVault is designed as a **modular security system** with clear separation of concerns.

---

## High-Level Architecture

Browser (UI)
↓
FastAPI Backend
↓
Security Modules
↓
Blockchain Audit Ledger


---

## Project Structure

app/
├── auth/ # Authentication + TOTP
├── messaging/ # Secure messaging
├── files/ # File encryption
├── blockchain/ # Audit ledger
├── core/ # Cryptographic primitives
├── templates/ # HTML user interface
└── main.py


---

## Modules

**Authentication Module**  
- Password hashing with Argon2  
- TOTP-based 2FA  
- Session management  

**Secure Messaging Module**  
- RSA key generation per user  
- Message encryption using public keys  
- Message decryption using private keys  

**File Encryption Module**  
- Per-user file encryption  
- Secure file storage  
- Controlled decryption  

**Blockchain Audit Ledger**  
- Immutable logging of security events  
- Proof-of-Work  
- Merkle tree validation  

---

## Design Principles

- Modularity  
- Defense in depth  
- Cryptography-first design  
- Auditability  


