import requests
import json
import os
from datetime import datetime
import get_time

device = os.environ.get('GOVEE_DEVICE')
api_key = os.environ.get('GOVEE_API_KEY')
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

    print('EVENT_TIME:', event_time)

    morning = to_time('07:00:00')

    morning_off_time = to_time('08:30:00')

    night_on_time = to_time('19:00:00')

    night_start = to_time('20:00:00')
    night_end = to_time('22:00:00')

    payload = {}

    if event_time == morning:
        payload = {
            "device": device,
            "model": model,
            "cmd": {
                "name": "color",
                "value": {
                    "r": 0,
                    "g": 255,
                    "b": 0
                }
            }
        }
    elif event_time == morning_off_time:
        payload = {
            "device": device,
            "model": model,
            "cmd": {
                "name": "turn",
                "value": "off"
            }
        }
    elif event_time == night_on_time:
        payload = {
            "device": device,
            "model": model,
            "cmd": {
                "name": "turn",
                "value": "on"
            }
        }
    elif night_start <= event_time <= night_end:
        payload = {
            "device": device,
            "model": model,
            "cmd": {
                "name": "color",
                "value": {
                    "r": 206,
                    "g": 0,
                    "b": 241
                }
            }
        }

    if payload:
        print('payload', payload)
        response = requests.put(url=control_url, data=json.dumps(payload), headers=headers)

        data = response.json()

        return {
            'statusCode': 200,
            'body': data
        }
    else:
        return {
            'statusCode': 200,
            'body': 'No changes'
        }
