import requests
import json
import os
from datetime import datetime
import get_time
import colors
from dotenv import load_dotenv

load_dotenv()

device = os.getenv('GOVEE_DEVICE')
api_key = os.getenv('GOVEE_API_KEY')
model = "H6003"
control_url = "https://developer-api.govee.com/v1/devices/control"

headers = {
    'Content-Type': 'application/json',
    'Govee-API-Key': api_key
}


def to_time(time):
    return_time = datetime.strptime(time, '%H:%M:%S').time()

    return return_time


def lambda_handler(event, context):
    event_time = get_time.get_time(event['time'])

    print('EVENT_TIME_CST:', event_time)

    morning = to_time('07:00:00')  # 01:00:00Z
    morning_off_time = to_time('08:30:00')  # 14:30:00Z
    night_on_time = to_time('19:00:00')  # 00:02:00Z
    night_start = to_time('20:00:00')  # 02:00:00Z
    night_end = to_time('22:00:00')  # 04:00:00Z

    payload = {
        "device": device,
        "model": model,
        "cmd": {}
    }

    if event_time == morning:
        payload.update({"cmd": {"name": "color", "value": colors.GREEN}})

    elif night_start <= event_time <= night_end:
        payload.update({"cmd": {"name": "color", "value": colors.PINK}})

    if payload.get("cmd"):
        print('payload', payload)
        response = requests.put(url=control_url, data=json.dumps(payload), headers=headers)

        data = response.json()

        if response.status_code != 200:
            raise Exception(data['message'])

        return {
            'statusCode': 200,
            'body': data,
        }
    else:
        return {
            'statusCode': 200,
            'body': 'No changes'
        }
