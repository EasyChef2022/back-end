from jwt import encode, decode


def generate_token(payload, secret):
    """Generate a JWT token"""
    return encode(payload=payload, key=secret, algorithm='HS256')


def decode_token(token, secret):
    """Decode a JWT token"""
    return decode(token, secret, algorithms=['HS256'])
