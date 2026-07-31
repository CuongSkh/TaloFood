from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import os
import jwt
from jwt import InvalidTokenError
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY

_password_hash = PasswordHasher()
_LEGACY_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def _verify_legacy_pbkdf2(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt_b64, digest_b64 = encoded.split('$', 3)
        if algorithm != 'pbkdf2_sha256':
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
        actual = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def verify_password(password: str, encoded: str) -> bool:
    if encoded.startswith('pbkdf2_sha256$'):
        return _verify_legacy_pbkdf2(password, encoded)
    try:
        return _password_hash.verify(encoded, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {'sub': str(subject), 'iat': now, 'exp': expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError as exc:
        raise ValueError('Token không hợp lệ hoặc đã hết hạn') from exc
