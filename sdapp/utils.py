import hashlib


def get_password_hash(password: str) -> str:
    return hashlib.sha256(bytes(password, "utf-8")).hexdigest()
