import base64
import hashlib
import hmac
import json
import time
from django.conf import settings

def _secret():
    return settings.SECRET_KEY.encode()

def create_qr_token(student_profile):
    """
    Creates a short-lived signed token.
    The student ID is encoded only as a server-verifiable payload;
    it is not exposed as a plain QR value.
    """
    now = int(time.time())
    bucket = now // settings.QR_VALIDITY_SECONDS
    payload = {
        "uid": student_profile.user_id,
        "bucket": bucket,
        "exp": (bucket + 1) * settings.QR_VALIDITY_SECONDS,
    }
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    encoded = base64.urlsafe_b64encode(raw).decode().rstrip("=")
    signature = hmac.new(_secret(), raw, hashlib.sha256).hexdigest()
    return f"{encoded}.{signature}"

def validate_qr_token(token):
    try:
        encoded, signature = token.split(".", 1)
        padding = "=" * (-len(encoded) % 4)
        raw = base64.urlsafe_b64decode((encoded + padding).encode())

        expected = hmac.new(_secret(), raw, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return None, "Invalid QR token."

        payload = json.loads(raw.decode())
        if int(time.time()) >= int(payload["exp"]):
            return None, "QR code expired. Ask the student to refresh their QR."

        # Only the current time bucket is accepted.
        current_bucket = int(time.time()) // settings.QR_VALIDITY_SECONDS
        if int(payload["bucket"]) != current_bucket:
            return None, "QR code expired. Ask the student to refresh their QR."

        return payload, None
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, base64.binascii.Error):
        return None, "Invalid QR token."


def qr_token_expiry(token):
    """Return the expiry timestamp embedded in a token for UI synchronization."""
    try:
        encoded, _ = token.split(".", 1)
        padding = "=" * (-len(encoded) % 4)
        raw = base64.urlsafe_b64decode((encoded + padding).encode())
        payload = json.loads(raw.decode())
        return int(payload["exp"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError,
            base64.binascii.Error, UnicodeDecodeError):
        return 0
