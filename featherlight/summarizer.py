import os
import json
from datetime import datetime
import subprocess

LOG_FILE = os.path.expanduser("~/.featherlight/log.json.enc")  # encrypted file
KEY_FILE = os.path.expanduser("~/.featherlight/key.key")

def summarize_logs():
    if not os.path.exists(LOG_FILE):
        print("No encrypted logs found for summarization.")
        return

    try:
        # Decrypt the logs (you can integrate decryptor logic if needed)
        from .encryptor import load_key
        from cryptography.fernet import Fernet

        key = load_key()
        fernet = Fernet(key)
        with open(LOG_FILE, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted).decode("utf-8")

        # Prepare logs for summarization
        lines = decrypted.strip().split("\n")
        logs = [json.loads(line) for line in lines]

        combined_text = "\n".join(
            f"[{log['timestamp']}] {log['activity']['app']} - {log['activity']['title']}"
            for log in logs
        )

        prompt = f"""
        ### SYSTEM PROMPT ###
        You are a local AI writing assistant called Feather-Light. Summarize the following activity logs as a diary entry, reflecting on the user's day in a clear, personal, and natural style.
        Logs:
        \n\n{combined_text}
        """

        print("[...] Summarizing logs using OpenHermes via Ollama...")
        print("This may lag for a few seconds... as we're using a local model for enhanced privacy.")
        result = subprocess.run(
        ["ollama", "run", "openhermes", prompt],
        capture_output=True,
        text=True
        )

        print("\n" + result.stdout.strip())

    except Exception as e:
        print(f"[!] Failed to summarize logs: {str(e)}")
