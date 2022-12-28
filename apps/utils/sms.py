import httpx
import asyncio

AUTH_URL = 'http://notify.eskiz.uz/api/auth/login'

URL = 'http://notify.eskiz.uz/api/message/sms/send'


def send_sms(phone, messsage, **kwargs):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'mobile_phone': phone,
        'message': messsage
    }

    response = httpx.post(AUTH_URL, headers=headers, data=payload)


async def auth_login(*args, **kwargs):
    payload = {
        'email': email,
        'password': password
    }

    response = httpx.post(AUTH_URL, data=payload)
    if response.status_code == 200:
        return response.json()['data']['token']

    await asyncio.sleep(5)
    token = await auth_login()


async def async_send_sms(*args, **kwargs):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'mobile_phone': phone,
        'message': message
    }

    response = httpx.post(AUTH_URL, headers=headers, data=payload)
    if not response.status_code == 200:
        await auth_login()
        print('You have error')
