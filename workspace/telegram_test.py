#!/usr/bin/env python3
import urllib.request
import json

TOKEN = "[TELEGRAM_BOT_TOKEN]"
MESSAGE = "System Online 💡💙"

# First, get updates to find the chat ID
def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data.get("ok") and data.get("result"):
                # Get the most recent chat ID
                for update in reversed(data["result"]):
                    if "message" in update:
                        return update["message"]["chat"]["id"]
                    elif "callback_query" in update:
                        return update["callback_query"]["message"]["chat"]["id"]
    except Exception as e:
        print(f"Error getting updates: {e}")
    return None

# Send the message
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

if __name__ == "__main__":
    print("Getting chat ID from Telegram...")
    chat_id = get_chat_id()
    if not chat_id:
        print("No active chat found. You need to message the bot first.")
        print("Message @umar_assistant_bot on Telegram, then run this again.")
        exit(1)
    
    print(f"Sending message to chat {chat_id}...")
    result = send_message(chat_id, MESSAGE)
    if result and result.get("ok"):
        print("Message delivered! Check your phone.")
    else:
        print(f"Failed: {result}")
