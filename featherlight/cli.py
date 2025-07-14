import argparse
from . import logger, encryptor, summarizer
from .logger import log_activity, loop_logging

def main():
    parser = argparse.ArgumentParser(
        description="Feather Press v1 - Invisible Logger & Local Summarizer"
    )
    parser.add_argument("--log", action="store_true", help="Log current activity once")
    parser.add_argument("--loop", type=int, help="Log activity every N seconds")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt the raw log file")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt and show the raw log file")
    parser.add_argument("--summarize", action="store_true", help="Summarize logs using local LLM")

    args = parser.parse_args()

    if args.log:
        from .logger import log_activity
        log_activity()

    if args.loop:
        from .logger import loop_logging
        loop_logging(args.loop)

    if args.encrypt:
        from .encryptor import encrypt_logs
        encrypt_logs()

    if args.decrypt:
        from .encryptor import decrypt_logs
        decrypt_logs()

    if args.summarize:
        from .summarizer import summarize_logs
        summarize_logs()
