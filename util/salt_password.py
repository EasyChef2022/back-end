import hashlib


def salt_password(password: str) -> str:
    salt = "EasyChef 2022"
    return hashlib.sha256((password + salt).encode()).hexdigest()


def compare_password(password, hashed_password) -> bool:
    return salt_password(password) == hashed_password
