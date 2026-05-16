import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
SALT = os.environ.get("SALT")

if not SALT:
    raise RuntimeError("SALT environment variable must be set")

def is_valid_email(email):
    """
    Basic validatation for registration email.

    Returns:
        Boolean
    """
    if not isinstance(email, str):
        return False

    if not email:
        return False

    email = email.strip()
    email_parts = email.split("@")

    if len(email_parts) != 2:
        return False

    local_part, domain_part = email_parts

    if not local_part or not domain_part:
        return False

    if "." not in domain_part:
        return False

    return True

def validate_password(password):
    """
    Basic validatation for registration password.

    Returns:
        str | None: An error message when invalid, otherwise None.
    """
    if not isinstance(password, str):
        return "Valid Password is required"

    if not password:
        return "Valid Password is required"

    if len(password) < 8:
        return "Password must be at least 8 characters"

    if len(password) > 128:
        return "Password must be 128 characters or fewer"

    if any(ord(char) < 32 or ord(char) > 126 for char in password):
        return "Password contains invalid characters"

    return None

def hash_password(password):
    salted_password = password + SALT
    hashed = hashlib.sha256(salted_password.encode())
    return hashed.hexdigest()

def get_bearer_token(auth_header):
    if not auth_header:
        return None

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.removeprefix("Bearer ").strip()

    if not token:
        return None

    return token