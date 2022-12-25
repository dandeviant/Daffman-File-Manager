from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = b'General Kenobi'

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.nonce
