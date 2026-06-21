import requests
import random
import string
import time
import threading
from discord_webhook import DiscordWebhook

# === CONFIG ===
WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1518203970911207424/sEvRQDY2P-GilzpVO-lRSI40djKnCiaaVO9txGo2jJmigIndR-MALDoWvSZ6AzJIBqoH"
THREADS = 20
# ==============

def send_webhook(code, type_nitro, valid=False):
    color = 0x00ff00 if valid else 0xff0000
    embed = {
        "title": "🎉 Nitro Found!" if valid else "Nitro Generated",
        "description": f"https://discord.gift/{code}",
        "color": color,
        "fields": [
            {"name": "Type", "value": type_nitro, "inline": True},
            {"name": "Valid", "value": str(valid), "inline": True}
        ]
    }
    webhook = DiscordWebhook(url=WEBHOOK_URL, embeds=[embed])
    try:
        webhook.execute()
    except:
        pass

def generate_code(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_code(code):
    try:
        r = requests.get(f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true", timeout=5)
        if r.status_code == 200:
            data = r.json()
            return True, data.get("promotion", {}).get("name", "Nitro")
        return False, None
    except:
        return False, None

def worker():
    while True:
        code = generate_code(16)
        valid, nitro_type = check_code(code)
        print(f"Checked: https://discord.gift/{code} | Valid: {valid}")
        if valid:
            print(f"✅ VALID NITRO FOUND: {code}")
            send_webhook(code, nitro_type or "Boost", True)
        else:
            send_webhook(code, "Nitro", False)
        time.sleep(0.1)

if __name__ == "__main__":
    print("Nitro Generator + Webhook Started...")
    for _ in range(THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
    input("Press Enter to stop...\n")
