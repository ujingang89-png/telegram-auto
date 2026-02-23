import os
import requests
import schedule
import time
from datetime import datetime
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

CHAT_ID_1 = "-1003539680106"
MESSAGE_1 = """일보 부탁드립니다~
1 2 3 4 5 6 7 8"""

CHAT_ID_2 = "-1002467111151"
MESSAGE_2 = "1 2 3 4 5 6 7 8"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, data=data)

def job():
    print("메시지 전송:", datetime.now())

    send_message(CHAT_ID_1, MESSAGE_1)
    send_message(CHAT_ID_2, MESSAGE_2)

schedule.every().day.at("12:00").do(job)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    job()  # 서버 시작하자마자 1번 전송 (테스트용)

    while True:
        schedule.run_pending()
        time.sleep(1)
