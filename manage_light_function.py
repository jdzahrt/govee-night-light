import requests
import json
import os
from datetime import datetime

device = os.environ.get('GOVEE_DEVICE')
api_key = os.environ.get('GOVEE_API_KEY')
model = "H6003"


def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Govee-API-Key': api_key
    }

    event_time = datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%SZ').time()

    morning = datetime.strptime('12:30:00', '%H:%M:%S').time()

    morning_off_time = datetime.strptime('14:30:00', '%H:%M:%S').time()

    night_on_time = datetime.strptime('00:00:00', '%H:%M:%S').time()

    night_start = datetime.strptime('01:00:00', '%H:%M:%S').time()
    night_end = datetime.strptime('03:00:00', '%H:%M:%S').time()

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
        control_url = "https://developer-api.govee.com/v1/devices/control"

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
