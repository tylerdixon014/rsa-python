import random
import math

# prime generator function (sieve of eratosthenes)
def eratosthenes():
    D = {}
    q = 2

    while True:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1

gen_primes = eratosthenes()

# generate keys 
    # public: (e,n)
    # private: (d,n)

# encryption / decryption

# main

for i in gen_primes:
    if i <= 1000:
        print(i)
    else:
        break