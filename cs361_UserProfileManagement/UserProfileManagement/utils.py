import requests
from django.conf import settings

def login_via_express(username, password):
    url = f"{settings.EXPRESS_AUTH_URL}/login"
    payload = {"username": username, "password": password}

    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json()  # contains accessToken and expiresAt
    except requests.exceptions.RequestException as e:
        print("Express login failed:", e)
        return None
