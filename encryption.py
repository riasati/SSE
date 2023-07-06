import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def KeyGen(k):
    random_class = random.Random(k)
    first_k = random_class.randint(1, 100)
    second_k = random_class.randint(1, 100)
    third_k = random_class.randint(1, 100)
    return first_k, second_k, third_k


def pseudo_random_permutation(key, list, index):
    random_class = random.Random(key)
    shuffle_list = random_class.sample(list, len(list))
    if index is None:
        return None
    return shuffle_list[index]


def pseudo_random_function(key, word, number_of_bits):
    random_class = random.Random(key)
    number = 0
    for char in word:
        number += ord(char)
    int_random_number = random_class.getrandbits(number)
    binary_random_number = bin(int_random_number)[2:]
    if len(binary_random_number) >= number_of_bits:
        return binary_random_number[:number_of_bits]
    else:
        return binary_random_number + ("0" * (number_of_bits - len(binary_random_number)))


# def encrypt_str(key, string):
#     cipher = AES.new(key, AES.MODE_ECB)
#     cipher_byte = cipher.encrypt(pad(string.encode("utf8"), AES.block_size))
#     cipher_text = b64encode(cipher_byte)
#     return f"{cipher_text.decode('utf8')}"
#
#
# def decrypt_str(key, string):
#     cipher_byte = b64decode(string)
#     decrypt_cipher = AES.new(key, AES.MODE_ECB)
#     plain_text = unpad(decrypt_cipher.decrypt(cipher_byte), AES.block_size)
#     return plain_text.decode("utf8")


def encrypt_str(key, string):
    cipher = AES.new(key, AES.MODE_CTR)
    #cipher_byte = cipher.encrypt(pad(string.encode("utf8"), AES.block_size))
    cipher_byte = cipher.encrypt(string.encode("utf8"))
    nonce = b64encode(cipher.nonce).decode('utf8')
    cipher_text = b64encode(cipher_byte).decode('utf8')
    return f"{cipher_text}||{nonce}"


def decrypt_str(key, string):
    split = string.split("||")
    data = split[0]
    nonce = split[1]
    nonce = b64decode(nonce)
    cipher_byte = b64decode(data)
    decrypt_cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    #plain_text = unpad(decrypt_cipher.decrypt(cipher_byte), AES.block_size)
    plain_text = decrypt_cipher.decrypt(cipher_byte)
    return plain_text.decode("utf8")


class Node:
    def __init__(self, record_id, key, permutation_output, nonce=None):
        self.nonce = nonce
        self.record_id = record_id
        self.key = key
        self.permutation_output = permutation_output

    def encrypt(self, key):
        cipher = AES.new(key, AES.MODE_CTR)
        cipher_text1 = cipher.encrypt(self.record_id.encode("utf8"))
        cipher_text2 = cipher.encrypt(self.key)
        cipher_text3 = cipher.encrypt(str(self.permutation_output).encode("utf8"))
        self.nonce = cipher.nonce
        return Node(cipher_text1, cipher_text2, cipher_text3, self.nonce)

    def decrypt(self, key):
        decrypt_cipher = AES.new(key, AES.MODE_CTR, nonce=self.nonce)
        plain_text1 = decrypt_cipher.decrypt(self.record_id).decode("utf8")
        plain_text2 = decrypt_cipher.decrypt(self.key)
        plain_text3 = decrypt_cipher.decrypt(self.permutation_output).decode("utf8")
        if plain_text3 != "None":
            plain_text3 = int(plain_text3)
        else:
            plain_text3 = None
        return Node(plain_text1, plain_text2, plain_text3, self.nonce)
