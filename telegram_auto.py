import os
import requests
import schedule
import time
from datetime import datetime
import pytz
from flask import Flask
import threading

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

CHAT_ID_1 = "-1003539680106"
MESSAGE_1 = """일보 부탁드립니다~
1 2 3 4 5 6 7 8"""

CHAT_ID_2 = "-1002467111151"
MESSAGE_2 = "1 2 3 4 5 6 7 8"

THREAD_ID_2 = 30

CHAT_ID_3 = "-1002467111151"
THREAD_ID_3 = 6
MESSAGE_3 = """주일 19시 전팀모임양식
올려주시면 감사하겠습니다!"""

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


def job_if_kst():
    global last_sent_date

    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    print("현재 KST:", kst)

    now_date = kst.strftime("%Y-%m-%d")

    if kst.strftime("%H:%M") in ["20:30", "20:31", "20:32"] and last_sent_date != now_date:
        last_sent_date = now_date

        send_message(CHAT_ID_1, MESSAGE_1)
        send_message(CHAT_ID_2, MESSAGE_2, THREAD_ID_2)

last_sent_date_sat = None

def job_saturday_2130():
    global last_sent_date_sat

    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    now_date = kst.strftime("%Y-%m-%d")

    if (
        kst.weekday() == 5 and  # 토요일
        kst.strftime("%H:%M") in ["21:30", "21:31", "21:32"] and
        last_sent_date_sat != now_date
    ):
        last_sent_date_sat = now_date
        send_message(CHAT_ID_3, MESSAGE_3, THREAD_ID_3)

schedule.every().minute.do(job_if_kst)
schedule.every().minute.do(job_saturday_2130)

@app.route('/')
def home():
    return "Bot is running!"


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


