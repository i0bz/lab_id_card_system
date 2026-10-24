import math

def is_prime(n: int) -> bool:
    upper_bound: int = int(math.sqrt(n)) + 1

    if n < 2:
        return False

    for x in range(2, upper_bound):
        if n % x == 0:
            return False
    return True



def euclid_gcd(a: int, b:int) -> int:

    if (b == 0):
        return a
    return euclid_gcd(b, a % b)


def extended_euclid(a: int, b: int) -> tuple[int, int, int]:
    
    if (b == 0):
        return a, 1, 0

    gcd, _x, _y = extended_euclid(b, a % b)
    x = _y
    y = _x - (a // b) * _y

    return gcd, x, y


def mod_inv(a: int, b:int) -> int:

    gcd, x, _ = extended_euclid(a, b)

    if (gcd != 1):
        raise ValueError("Modular Inverse does not exist!!!")
    return x % b

