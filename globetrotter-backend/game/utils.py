from rest_framework.response import Response
from rest_framework.decorators import api_view
from urllib.parse import quote
import random
import hashlib
from .models import User
import qrcode
import os

GAME_BASE_URL = "http://127.0.0.1:8000/play"

def generate_shareable_link(username, friend_username):
    """Generate a unique shareable link using a hash."""
    unique_id = hashlib.md5(f"{username}-{friend_username}".encode()).hexdigest()[:8]
    return f"{GAME_BASE_URL}?invite={unique_id}&user={quote(username)}"

def generate_qr_code(url):
    """Generate a QR code for the invite link."""
    qr = qrcode.make(url)
    qr_path = f"static/qrcodes/{hashlib.md5(url.encode()).hexdigest()}.png"
    
    os.makedirs("static/qrcodes", exist_ok=True)
    qr.save(qr_path)
    
    return qr_path