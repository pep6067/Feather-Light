import os
from cryptography.fernet import Fernet

KEY_FILE = os.path.expanduser("~/.featherlight/key.key")
RAW_FILE = os.path.expanduser("~/.featherlight/log.json")
ENC_FILE = os.path.expanduser("~/.featherlight/log.json.enc")

def generate_key():
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_logs():
    if not os.path.exists(RAW_FILE):
        print("[!] No raw log file to encrypt.")
        return
    key = load_key()
    fernet = Fernet(key)
    with open(RAW_FILE, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(ENC_FILE, "wb") as f:
        f.write(encrypted)
    os.remove(RAW_FILE)
    print("[✓] Logs encrypted and raw file removed.")

def decrypt_logs():
    if not os.path.exists(ENC_FILE) or not os.path.exists(KEY_FILE):
        print("No files are there to decrypt.")
        return
    try:
        key = load_key()
        fernet = Fernet(key)
        with open(ENC_FILE, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
        print(decrypted.decode("utf-8"))
    except Exception as e:
        print("No files are there to decrypt.")
