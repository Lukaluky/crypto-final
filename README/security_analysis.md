# CryptoVault – Security Analysis

This document describes potential threats and their mitigations.

---

## Threat Model

**1. Password Theft**  
- **Threat:** Attacker steals the database  
- **Mitigation:**  
  - Argon2 password hashing  
  - No plaintext passwords stored  

**2. Account Takeover**  
- **Threat:** Stolen credentials  
- **Mitigation:**  
  - TOTP-based 2FA  
  - Integration with Google Authenticator  

**3. Message Interception**  
- **Threat:** Man-in-the-middle attack  
- **Mitigation:**  
  - RSA encryption of messages  
  - Messages stored only in encrypted form  

**4. File Tampering**  
- **Threat:** Unauthorized file access  
- **Mitigation:**  
  - Encrypted files with user-specific keys  

**5. Log Manipulation**  
- **Threat:** Deleting or editing logs  
- **Mitigation:**  
  - Blockchain audit ledger  
  - Hash chaining and Proof-of-Work  

---

## Security Conclusion

CryptoVault applies **layered security**:  

- Strong cryptography  
- Secure authentication  
- Auditability via blockchain
