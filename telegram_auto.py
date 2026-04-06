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

CHAT_ID_4 = "-1002244734007"
MESSAGE_4 = "파트별 금주 논의사항 양식 올려주세요~!"

CHAT_ID_5 = "-1002244734007"
MESSAGE_5 = "주간회의 PPT 마무리해주세요~!"

CHAT_ID_JS = "-1003851451653"

MSG_MON_10 = "부장님 이번주 진성신 범위는 어디일까요?"
MSG_TUE = "진성신은 목요일 주간회의 전까지입니다."
MSG_WED = "진성신은 목요일까지입니다, 주간회의 전까지 입니다."
MSG_THU = "당일에 주시는 사유보고는 받지 않겠습니다. 주간회의 전까지 모두 마무리 부탁드립니다."

# 느낀점 방
CHAT_ID_FEEL = "-1002697448961"

MSG_MON_FEEL = "교육 들으신 분들은 느낀점 마무리 해주시고 수정해주세요"
MSG_TUE_FEEL = "교육 들으신 분들은 느낀점 마무리 해주시고 수정해주세요"
MSG_WED_FEEL = "청취 요일 수정과 느낀점 마무리 해주세요. 토요일까지입니다!"
MSG_THU_FEEL = "토요일까지입니다. 모두 시간 맞춰 청취 부탁드립니다. 요일 수정해주세요"
MSG_FRI_FEEL = "교육과 주간회의는 모두 토요일까지입니다. 모두 시간 맞춰 청취 부탁드립니다. 요일 수정해주세요"
MSG_SAT_FEEL = """토요일까지 모두 완료해주세요!
오늘까지 마무리 부탁드립니다.
일요일까지도 이름 남아있는 사명자는 사유 물어보겠습니다.
사유보고는 당일이 아닌, 미리 하는것이 사유보고입니다.
당일에 사유보고 하신분들은 사유보고로 받지 않겠습니다."""

CHAT_ID_WORSHIP = "-1002058115709"
MSG_MON_WORSHIP = "구역예배 시간 올려주세요"
MSG_TUE_WORSHIP = "구역예배 시간 올려주세요! 구역예배 교안은 금요일 오전 8시까지입니다. 8:01분이 될시에도 벌금입니다!"
MSG_WED_WORSHIP = "구역예배 교안은 금요일 오전 8시까지입니다. 8:01분이 될시에도 벌금입니다!"
MSG_THU_WORSHIP = "구역예배 교안은 금요일 오전 8시까지입니다. 8:01분이 될시에도 벌금입니다!"
MSG_FRI_WORSHIP = "구역예배 교안 시간이 얼마 남지 않았습니다. 8:01분 되면 벌금입니다!"

def send_message(chat_id, text, thread_id=None):
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}

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
        
last_sent_date_thu = None

def job_thursday_2300():
    global last_sent_date_thu

    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    now_date = kst.strftime("%Y-%m-%d")

    if (
        kst.weekday() == 3 and
        kst.strftime("%H:%M") in ["23:00", "23:01", "23:02"] and
        last_sent_date_thu != now_date
    ):
        last_sent_date_thu = now_date
        send_message(CHAT_ID_4, MESSAGE_4)

last_sent_date_wed = None

def job_wednesday_2300():
    global last_sent_date_wed

    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    now_date = kst.strftime("%Y-%m-%d")

    if (
        kst.weekday() == 2 and
        kst.strftime("%H:%M") in ["23:00", "23:01", "23:02"] and
        last_sent_date_wed != now_date
    ):
        last_sent_date_wed = now_date
        send_message(CHAT_ID_5, MESSAGE_5)

last_sent_mon = None
def job_monday_10():
    global last_sent_mon
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    now_date = kst.strftime("%Y-%m-%d")
    if kst.weekday() == 0 and kst.strftime("%H:%M") == "10:00" and last_sent_mon != now_date:
        last_sent_mon = now_date
        send_message(CHAT_ID_JS, MSG_MON_10)

last_sent_tue = None
def job_tuesday():
    global last_sent_tue
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    now_date = kst.strftime("%Y-%m-%d")
    if kst.weekday() == 1 and kst.strftime("%H:%M") in ["10:00", "20:00"] and last_sent_tue != now_date:
        last_sent_tue = now_date
        send_message(CHAT_ID_JS, MSG_TUE)

last_sent_wed = None
def job_wednesday():
    global last_sent_wed
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    now_date = kst.strftime("%Y-%m-%d")
    if kst.weekday() == 2 and kst.strftime("%H:%M") in ["10:00", "20:00"] and last_sent_wed != now_date:
        last_sent_wed = now_date
        send_message(CHAT_ID_JS, MSG_WED)

last_sent_thu = None
def job_thursday():
    global last_sent_thu
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    now_date = kst.strftime("%Y-%m-%d")
    if kst.weekday() == 3 and kst.strftime("%H:%M") in ["10:00", "15:00", "21:00"] and last_sent_thu != now_date:
        last_sent_thu = now_date
        send_message(CHAT_ID_JS, MSG_THU)

last_sent_feel_mon = None
def job_feel_monday():
    global last_sent_feel_mon
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 0:  # 월요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") == "21:00" and last_sent_feel_mon != now_date:
            last_sent_feel_mon = now_date
            send_message(CHAT_ID_FEEL, MSG_MON_FEEL)


last_sent_feel_tue = None
def job_feel_tuesday():
    global last_sent_feel_tue
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 1:  # 화요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["10:00", "18:00"] and last_sent_feel_tue != now_date:
            last_sent_feel_tue = now_date
            send_message(CHAT_ID_FEEL, MSG_TUE_FEEL)


last_sent_feel_wed = None
def job_feel_wednesday():
    global last_sent_feel_wed
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 2:  # 수요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["10:00", "18:00"] and last_sent_feel_wed != now_date:
            last_sent_feel_wed = now_date
            send_message(CHAT_ID_FEEL, MSG_WED_FEEL)


last_sent_feel_thu = None
def job_feel_thursday():
    global last_sent_feel_thu
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 3:  # 목요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["10:00", "18:00"] and last_sent_feel_thu != now_date:
            last_sent_feel_thu = now_date
            send_message(CHAT_ID_FEEL, MSG_THU_FEEL)


last_sent_feel_fri = None
def job_feel_friday():
    global last_sent_feel_fri
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 4:  # 금요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["10:00", "18:00"] and last_sent_feel_fri != now_date:
            last_sent_feel_fri = now_date
            send_message(CHAT_ID_FEEL, MSG_FRI_FEEL)


last_sent_feel_sat = None
def job_feel_saturday():
    global last_sent_feel_sat
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 5:  # 토요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["10:00", "15:00", "19:00", "21:00", "23:00"] and last_sent_feel_sat != now_date:
            last_sent_feel_sat = now_date
            send_message(CHAT_ID_FEEL, MSG_SAT_FEEL)

last_sent_worship_mon = None
def job_worship_monday():
    global last_sent_worship_mon
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 0:  # 월요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["10:00", "20:00"] and last_sent_worship_mon != now_date:
            last_sent_worship_mon = now_date
            send_message(CHAT_ID_WORSHIP, MSG_MON_WORSHIP)

last_sent_worship_tue = None
def job_worship_tuesday():
    global last_sent_worship_tue
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 1:  # 화요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["11:00", "20:00"] and last_sent_worship_tue != now_date:
            last_sent_worship_tue = now_date
            send_message(CHAT_ID_WORSHIP, MSG_TUE_WORSHIP)

last_sent_worship_wed = None
def job_worship_wednesday():
    global last_sent_worship_wed
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 2:  # 수요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["10:00", "18:00"] and last_sent_worship_wed != now_date:
            last_sent_worship_wed = now_date
            send_message(CHAT_ID_WORSHIP, MSG_WED_WORSHIP)

last_sent_worship_thu = None
def job_worship_thursday():
    global last_sent_worship_thu
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 3:  # 목요일
        now_date = kst.strftime("%Y-%m-%d")

        if kst.strftime("%H:%M") in ["10:00", "20:00", "23:00", "00:00"] and last_sent_worship_thu != now_date:
            last_sent_worship_thu = now_date
            send_message(CHAT_ID_WORSHIP, MSG_THU_WORSHIP)

last_sent_worship_fri = None
def job_worship_friday():
    global last_sent_worship_fri
    kst = datetime.now(pytz.timezone("Asia/Seoul"))
    if kst.weekday() == 4:  # 금요일
        now_date = kst.strftime("%Y-%m-%d")
        if kst.strftime("%H:%M") in ["05:00", "06:00", "07:00"] and last_sent_worship_fri != now_date:
            last_sent_worship_fri = now_date
            send_message(CHAT_ID_WORSHIP, MSG_FRI_WORSHIP)



schedule.every().minute.do(job_if_kst)
schedule.every().minute.do(job_saturday_2130)
schedule.every().minute.do(job_thursday_2300)
schedule.every().minute.do(job_wednesday_2300)

schedule.every().minute.do(job_monday_10)
schedule.every().minute.do(job_tuesday)
schedule.every().minute.do(job_wednesday)
schedule.every().minute.do(job_thursday)

schedule.every().minute.do(job_feel_monday)
schedule.every().minute.do(job_feel_tuesday)
schedule.every().minute.do(job_feel_wednesday)
schedule.every().minute.do(job_feel_thursday)
schedule.every().minute.do(job_feel_friday)
schedule.every().minute.do(job_feel_saturday)

schedule.every().minute.do(job_worship_monday)
schedule.every().minute.do(job_worship_tuesday)
schedule.every().minute.do(job_worship_wednesday)
schedule.every().minute.do(job_worship_thursday)
schedule.every().minute.do(job_worship_friday)


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




