import os
import json

import telegram

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret File Control
telegram_file = os.path.join(BASE_DIR, "bot_info.json")

with open(telegram_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        erro_msg = f"Set the {setting} environment variable"
        raise ImproperlyConfigured(erro_msg)

def send_msg(msg):
    test_token = get_secret("demo_token")
    test_bot = telegram.Bot(token=test_token)
    test_room = get_secret("demo_id")

    test_bot.sendMessage(chat_id=test_room, text=msg)
