# app/auth/totp.py
# TOTP implementation

import pyotp


def generate_totp_secret():
    return pyotp.random_base32()


def verify_totp(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
