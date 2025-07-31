import random
import math

e = 65537

# prime generator function (sieve of eratosthenes)

import random

def is_Prime(n):
    if n != int(n):
        return False
    n = int(n)
    
    if n == 0 or n == 1 or n == 3 or n == 4 or n == 6 or n == 8 or n == 9:
        return False
    if n == 2 or n == 5 or n == 7:
        return True
    
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert(2 ** s * d == n-1)
    
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True
    
    for i in range(8):  #number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
        
    return True

def random_Prime(bits):
    lower_bound = 2 ** (bits - 1)
    upper_bound = 2 ** bits

    p = random.randrange(lower_bound,upper_bound)
    while is_Prime(p) == False:
        p = random.randrange(lower_bound,upper_bound)

    return p

# generate keys 
def extended_gcd(a,b):  # extended euclidean algorithm
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
def modinv(a, m): # modular inverse function
    g, x, y = extended_gcd(a,m)
    if g!= 1:
        raise Exception("Modular inverse DNE")
    else:
        return x % m

def generate_keys(bits):
    p = random_Prime(bits)
    q = random_Prime(bits)
    while p == q:
        q = random_Prime(bits)

    n = p * q
    totient = (p - 1) * (q - 1)
    d = modinv(e, totient)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

# encryption / decryption
def encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message.encode(),'big')

    if message_int >= n:
        raise ValueError("Message is too long.")

    ciphertext = pow(message_int, e, n)
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    message_int = pow(ciphertext, d, n)
    message_bytes = int.to_bytes(message_int,(message_int.bit_length() + 7) // 8, 'big')
    return message_bytes.decode()

# main

def main():
    public_key, private_key = generate_keys(int(input("How many bits of encryption? (Over 16 bits will have a long computation time): ")))
    print("Public key:", public_key)
    print("Private key:", private_key)

    ciphertext = encrypt(input("Message to be encrypted: "), public_key)
    print("Encrypted message:", ciphertext)

    message_decrypted = decrypt(ciphertext, private_key)
    print("Decrypted message:", message_decrypted)

if __name__ == "__main__":
    main()