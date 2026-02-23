import requests
import schedule
import time
from flask import Flask
import threading

TOKEN = "8703437303:AAHvITyXQjo8YopZWe9x_xHgO8-0hBFcZvw"
CHAT_ID = "-1003539680106"

def send_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "무료 서버에서 자동 메시지 테스트!"
    }
    requests.post(url, data=data)

schedule.every().day.at("12:00").do(send_message)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(30)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

threading.Thread(target=run_schedule).start()
send_message()  # 서버 시작 시 1회 전송

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


