from enum import Enum
from . import utils

class key_type(Enum):
    PUBLIC = 1
    PRIVATE = 2


class rsa_key:
    def __init__(self, modulus: int, exponent: int, type: key_type):
        self.modulus = modulus
        self.exponent = exponent
        self.type = type




def encrypt(key: rsa_key, payload: str) -> list[int]:
    if key.type != key_type.PUBLIC:
        raise TypeError("Invalid Argument!!!")

    encrypted_data: list[int] = []

    for x in payload:
        encrypted_data.append((ord(x) ** key.exponent) % key.modulus)

    return encrypted_data

def decrypt(key: rsa_key, payload: list[int]) -> str:
    if key.type != key_type.PRIVATE:
        raise TypeError("Invalid Argument!!!")

    decrypted_data: str = ""


    for x in payload:
        decrypted_data += chr((x ** key.exponent) % key.modulus)

    return decrypted_data


def generate_keys(p: int, q: int, public_exponent: int) -> tuple[rsa_key, rsa_key]:
    if (p == q):
        raise ValueError("Primes must be distint!!!")

    if (not utils.is_prime(p) or not utils.is_prime(q)):
        raise ValueError("Not a valid prime!!!")

    modulus: int = p * q

    if (modulus < 256):
        raise ValueError("Modulus cannot accomodate for Extended ASCII characters!!!")

    totient: int = (p - 1) * (q - 1)

    if (modulus < 127):
        raise ValueError("Given primes cannot handle all ASCII values!!!")

    if utils.euclid_gcd(public_exponent, totient) != 1:
        raise ValueError("Public Exponent is not coprime to the totient!!!")

    private_exponent = utils.mod_inv(public_exponent,totient)


    return rsa_key(modulus, public_exponent, key_type.PUBLIC), rsa_key(modulus, private_exponent, key_type.PRIVATE)

