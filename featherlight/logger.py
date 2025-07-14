import os
import json
import psutil
import win32gui
import win32process
from datetime import datetime
from urllib.parse import unquote
import winreg
import time  # for loop_logging

LOG_FILE = os.path.expanduser("~/.featherlight/log.json")

def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        app_name = proc.name()
        title = win32gui.GetWindowText(hwnd)
        print(f"[DEBUG] Active window detected: {app_name} - {title}")
        return {"app": app_name, "title": title}
    except Exception as e:
        print(f"[ERROR] Failed to get active window: {e}")
        return {"app": "Unknown", "title": "Unknown"}

def get_chrome_profile_paths():
    paths = []
    try:
        key_path = r"Software\Google\Chrome\PreferenceMACs"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                name = winreg.EnumKey(key, i)
                profile_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\{}".format(name))
                if os.path.exists(profile_path):
                    paths.append(profile_path)
        print(f"[DEBUG] Chrome profiles found: {paths}")
    except Exception as e:
        print(f"[ERROR] Failed to get Chrome profiles: {e}")
    return paths

def get_browser_tabs_chrome_style(profile_paths):
    tabs = []
    for profile_path in profile_paths:
        current_tabs_path = os.path.join(profile_path, "Current Tabs")
        if os.path.exists(current_tabs_path):
            try:
                with open(current_tabs_path, "rb") as f:
                    data = f.read()
                    data_str = data.decode('latin1', errors='ignore')
                    for line in data_str.split("\x00"):
                        if line.startswith("http") or line.startswith("https"):
                            tabs.append(unquote(line))
            except Exception as e:
                print(f"[ERROR] Failed to read tabs from {current_tabs_path}: {e}")
                continue
    print(f"[DEBUG] Chrome tabs found: {tabs[:10]}")
    return tabs[:10]

def get_firefox_tabs():
    import lz4.block
    tabs = []
    appdata = os.getenv("APPDATA")
    ff_path = os.path.join(appdata, "Mozilla", "Firefox", "Profiles")
    if not os.path.exists(ff_path):
        print("[DEBUG] Firefox profiles folder not found.")
        return tabs
    profiles = [os.path.join(ff_path, d) for d in os.listdir(ff_path) if os.path.isdir(os.path.join(ff_path, d))]
    for profile in profiles:
        recovery_file = os.path.join(profile, "sessionstore-backups", "recovery.jsonlz4")
        if os.path.exists(recovery_file):
            try:
                with open(recovery_file, "rb") as f:
                    magic = f.read(8)
                    if magic != b'mozLz40\0':
                        continue
                    compressed = f.read()
                    decompressed = lz4.block.decompress(compressed)
                    session = json.loads(decompressed)
                    windows = session.get("windows", [])
                    for window in windows:
                        for tab in window.get("tabs", []):
                            entries = tab.get("entries", [])
                            if entries:
                                url = entries[-1].get("url", "")
                                tabs.append(url)
            except Exception as e:
                print(f"[ERROR] Failed to parse Firefox tabs from {recovery_file}: {e}")
                continue
    print(f"[DEBUG] Firefox tabs found: {tabs[:10]}")
    return tabs[:10]

def get_all_browser_tabs():
    tabs = []
    tabs.extend(get_browser_tabs_chrome_style(get_chrome_profile_paths()))
    tabs.extend(get_firefox_tabs())
    print(f"[DEBUG] Total tabs collected: {len(tabs[:15])}")
    return tabs[:15]

def log_activity():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    print("[DEBUG] Starting to log activity...")
    active = get_active_window()
    browser_tabs = get_all_browser_tabs()
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "activity": active,
        "browser_tabs": browser_tabs
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"[✓] Logged {log_entry['timestamp']}: {active['app']} - {active['title']} with {len(browser_tabs)} tabs")

def loop_logging(interval):
    try:
        print(f"[⏳] Starting continuous logging every {interval} seconds. Press Ctrl+C to stop.")
        while True:
            log_activity()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[✋] Logging stopped by user.")
