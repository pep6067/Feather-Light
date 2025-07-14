import os
import sys
import subprocess
import platform

def run_cmd(cmd, shell=True, capture_output=False):
    print(f"\033[96m>>> Running:\033[0m {cmd}")
    return subprocess.run(cmd, shell=shell, capture_output=capture_output, text=True)

def print_header():
    print("\n" + "="*60)
    print("\033[95m The FeatherLight Company — FeatherLight-v1 Installation Wizard \033[0m")
    print("="*60 + "\n")

def check_ollama():
    try:
        run_cmd("ollama --version", capture_output=True)
        print("\033[92m[✓] Ollama CLI is installed!\033[0m")
        return True
    except Exception:
        print("\033[91m[✗] Ollama CLI NOT found.\033[0m")
        print("Please install Ollama from https://ollama.com and add it to your PATH.")
        return False

def check_openhermes():
    result = run_cmd("ollama list", capture_output=True)
    if result.returncode != 0:
        print("\033[91m[✗] Failed to check Ollama models.\033[0m")
        return False
    models = result.stdout.lower()
    return "openhermes" in models

def install_openhermes():
    print("\nOpenHermes model (~4.1 GiB) is not installed locally.")
    choice = input("Do you want to install OpenHermes now? (y/n): ").strip().lower()
    if choice != "y":
        print("OpenHermes installation skipped. FeatherLight will use default model.")
        return False

    print("\nDownloading OpenHermes model. This may take a while and consume disk space...\n")
    result = run_cmd("ollama pull openhermes")
    if result.returncode == 0:
        print("\033[92m[✓] OpenHermes installed successfully!\033[0m\n")
        return True
    else:
        print("\033[91m[✗] Failed to install OpenHermes.\033[0m\n")
        return False

def print_activation_instructions():
    print("\n[!] Please activate your virtual environment BEFORE continuing.")
    if platform.system() == "Windows":
        print(r"   PowerShell: .\venv\Scripts\Activate.ps1")
        print(r"   CMD:       venv\Scripts\activate.bat")
    else:
        print("   Run: source ./venv/bin/activate")

def main():
    print_header()

    if not os.path.exists("venv"):
        print("[*] Creating virtual environment (venv)...")
        run_cmd(f'"{sys.executable}" -m venv venv')
        print_activation_instructions()
        input("\nPress Enter after activating the virtual environment...")
    else:
        print("[*] Virtual environment already exists.\n")
        print_activation_instructions()
        print("\nYou should activate it now before continuing.\n")
        input("Press Enter once venv is activated...")

    # Upgrade pip
    print("\n[*] Upgrading pip to latest version...")
    if platform.system() == "Windows":
        run_cmd(r'venv\Scripts\python.exe -m pip install --upgrade pip')
    else:
        run_cmd('venv/bin/python -m pip install --upgrade pip')

    # Install your package in editable mode
    print("\n[*] Installing FeatherLight package in editable mode...")
    if platform.system() == "Windows":
        run_cmd(r'venv\Scripts\python.exe -m pip install -e .')
    else:
        run_cmd('venv/bin/python -m pip install -e .')

    # Check Ollama CLI presence
    if not check_ollama():
        print("\n\033[91m[✗] Ollama CLI is required for FeatherLight to function.\033[0m\n")
        print("Installation incomplete.")
        sys.exit(1)

    # Check OpenHermes model presence
    has_openhermes = check_openhermes()
    if not has_openhermes:
        has_openhermes = install_openhermes()

    # Ensure Ollama daemon is running (usually auto-started)
    print("[*] Ensuring Ollama daemon is running (usually auto-started)...")
    run_cmd("ollama status")

    print("\n\033[96mInstallation complete!\033[0m")
    print("You can now run FeatherLight inside your activated venv.\n")
    print("Try:\n  featherlight --help\n")

    if has_openhermes:
        print("FeatherLight will use OpenHermes model for richer diary-style summaries.\n")
    else:
        print("FeatherLight will use default CodeLlama model.\n")
print("Start your venv by running:\n  PowerShell: .\venv\Scripts\Activate.ps1\n \n CMD:       venv\Scripts\activate.bat\n")  
print("\033[93m[!] Remember to activate your virtual environment before running FeatherLight!\033[0m\n")
if __name__ == "__main__":
    main()
