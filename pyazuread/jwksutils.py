import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def ensure_bytes(key):
    """
    If the key is a string, encode it as UTF-8 bytes
    
    :param key: The key to use for the hash
    :return: The key is being encoded to bytes.
    """
    if isinstance(key, str):
        key = key.encode('utf-8')
    return key


def decode_value(val):
    """
    It takes a base64 encoded string, decodes it, and returns the decoded value as an integer
    
    :param val: The value to decode
    :return: The decoded value of the token.
    """
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b'==')
    return int.from_bytes(decoded, 'big')


def rsa_pem_from_jwk(jwk):
    """
    It takes a JWK and returns a PEM
    
    :param jwk: The JWK you want to convert to PEM
    :return: A PEM encoded RSA public key.
    """
    return RSAPublicNumbers(
        n=decode_value(jwk['n']),
        e=decode_value(jwk['e'])
    ).public_key(default_backend()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )