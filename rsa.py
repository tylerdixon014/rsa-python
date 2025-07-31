import random
import math

e = 65537

# prime generator function (sieve of eratosthenes)
def sieve(limit):
    D = {}
    q = 2

    while q <= limit:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1

def random_prime(bit_length):
    lower_bound = 2**(bit_length - 1)
    upper_bound = 2**(bit_length)

    primes = sieve(upper_bound)
    valid_primes = [p for p in primes if lower_bound <= p]

    if not valid_primes:
        print("There are no valid primes of the desired bit length")

    return random.choice(valid_primes)

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

def generate_keys(bit_length):
    p = random_prime(bit_length)
    q = random_prime(bit_length)
    while p == q:
        q = random_prime(bit_length)

    n = p * q
    totient = (p - 1) * (q - 1)
    d = modinv(e, totient)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

# encryption / decryption
def encrypt(message, public_key):
    e, n = public_key
    message_encoded = int.from_bytes(message.encode())
    ciphertext = pow(message_encoded, e, n)
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    message_encoded = int.to_bytes(pow(ciphertext, d, n))
    return message_encoded.decode()

# main

def main():
    public_key, private_key = generate_keys(int(input("How many bits of encryption? (Over 16 bits will have a long computation time): ")))
    print("Public key:", public_key)
    print("Private key:", private_key)

    ciphertext = encrypt(input("Message to be encrypted: "), public_key)
    print("Encrypted message:", ciphertext)

    message_decrypted = decrypt(ciphertext, private_key)
    print("Decrypted message:", message_decrypted)

main()