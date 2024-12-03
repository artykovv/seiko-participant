
import random
import string


async def generate_code():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    digits = ''.join(random.choices(string.digits, k=3))
    return letters + digits