import requests
from django.conf import settings


def send_otp_sms(phone, otp):
    """
    Send OTP to user's registered mobile number using MSG91
    """
    if settings.DEBUG:
        # During development, avoid real SMS cost
        print(f"[DEV MODE] OTP for {phone}: {otp}")
        return

    url = "https://control.msg91.com/api/v5/otp"

    payload = {
        "mobile": f"91{phone}",
        "otp": otp,
        "template_id": settings.MSG91_TEMPLATE_ID,
    }

    headers = {
        "authkey": settings.MSG91_AUTH_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
