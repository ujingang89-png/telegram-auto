import requests

# ====== 설정 ======
TOKEN = "8703437303:AAHvITyXQjo8YopZWe9x_xHgO8-0hBFcZvw"
CHAT_ID = "-1003539680106"
MESSAGE = """일보 부탁드립니다~ 
1 2 3 4 5 6 7 8"""
# ==================

def send_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": MESSAGE
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("메시지 전송 성공")
    else:
        print("전송 실패:", response.text)

if __name__ == "__main__":
    send_message()