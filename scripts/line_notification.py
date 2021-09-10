import os

import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')
NOTIFY_API = 'https://notify-api.line.me/api/notify'

def notify_line(message: str):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    data = {
        'message': message,
    }
    res = requests.post(
        url=NOTIFY_API,
        data=data,
        headers=headers
    )
    if res.json()["status"] != 200:
        print('Line通知に失敗しました')
