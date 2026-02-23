import os
import requests
import schedule
import time
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

CHAT_ID_1 = "-1003539680106"
MESSAGE_1 = """일보 부탁드립니다~
1 2 3 4 5 6 7 8"""

CHAT_ID_2 = "-1002467111151"
MESSAGE_2 = "1 2 3 4 5 6 7 8"

THREAD_ID_2 = 30

def send_message(chat_id, text, thread_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if thread_id is not None:
        data["message_thread_id"] = thread_id

    requests.post(url, data=data)

last_sent_date = None

def job_if_kst_2100():
    global last_sent_date

    kst = datetime.utcnow() + timedelta(hours=9)

    print("현재 KST:", kst)

    now_date = kst.strftime("%Y-%m-%d")

    if kst.strftime("%H:%M") == "21:00" and last_sent_date != now_date:
        last_sent_date = now_date

        send_message(CHAT_ID_1, MESSAGE_1)
        send_message(CHAT_ID_2, MESSAGE_2, THREAD_ID_2)

schedule.every().minute.do(job_if_kst_2100)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)

