import os
from uuid import uuid4

import requests

AUTH_URL = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
SALUTE_SPEECH_AUTH_DATA_BASE64 = os.getenv('SALUTE_SPEECH_AUTH_DATA')


async def get_access_token():
    url = AUTH_URL
    headers = {
        'Authorization': f'Basic {SALUTE_SPEECH_AUTH_DATA_BASE64}',
        'RqUID': str(uuid4()),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'scope': 'SALUTE_SPEECH_PERS'
    }
    response = requests.post(url, headers=headers, data=body, verify=False)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
