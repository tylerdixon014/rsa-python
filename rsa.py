import random
import math
import tkinter as tk
from tkinter import *
from tkinter import ttk

e = 65537

# prime generator function (miller-rabin primality test)
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
    try:
        message_int = int.from_bytes(message.encode(),'big')
    except ValueError:
        print("Encoding error")
    

    if message_int >= n:
        raise ValueError("Message is too long.")

    try:
        ciphertext = pow(message_int, e, n)
    except ValueError:
        print("Encryption error")
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    try:
        message_int = pow(ciphertext, d, n)
    except ValueError:
        print("Decryption error")
    message_bytes = int.to_bytes(message_int,(message_int.bit_length() + 7) // 8, 'big')
    try:
        return message_bytes.decode()
    except ValueError:
        print("Decoding error")
# gui

class gui_Encrypt:

    def __init__(self, root):

        root.title("Encryption and Decryption")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
       
        self.message = StringVar()
        message_entry = ttk.Entry(mainframe, width=7, textvariable=self.message)
        message_entry.grid(column=2, row=1, sticky=W)

        self.bits = StringVar()
        bits_entry = ttk.Entry(mainframe, width=7, textvariable=self.bits)
        bits_entry.grid(column=4, row=1, sticky=W)

        self.public_key = StringVar()
        self.private_key = StringVar()
        self.ciphertext = StringVar()
        self.message_deciphered = StringVar()
        self.error_message = StringVar()

        ttk.Label(mainframe, textvariable=self.public_key).grid(column=2, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.private_key).grid(column=2, row=3, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.ciphertext).grid(column=2, row=4, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.message_deciphered).grid(column=2, row=5, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.error_message).grid(column=2, row=6, sticky=(W, E))

        ttk.Button(mainframe, text="Encrypt", command=self.gui_encrypt).grid(column=5, row=1, sticky=W)

        ttk.Label(mainframe, text="Message:").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Bits:").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="Public Key:").grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text="Private Key:").grid(column=1, row=3, sticky=W)
        ttk.Label(mainframe, text="Encrypted Message:").grid(column=1, row=4, sticky=W)
        ttk.Label(mainframe, text="Decrypted Message:").grid(column=1, row=5, sticky=W)
        ttk.Label(mainframe, text="Error:").grid(column=1, row=6, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        bits_entry.focus()
        message_entry.focus()
        root.bind("<Return>", self.gui_encrypt)

    def gui_encrypt(self, *args):
        try:
            public_key, private_key = generate_keys(int(self.bits.get()))
            ciphertext = encrypt(self.message.get(), public_key)
            self.public_key.set(public_key)
            self.private_key.set(private_key)
            self.ciphertext.set(ciphertext)
            self.error_message.set("")
        except ValueError:
            self.error_message.set("There was an error")

root = Tk()
gui_Encrypt(root)
root.mainloop()

# bits_input = int(input("Bits:"))
# message_input = input("Message:")
# sample_public_key, sample_private_key = generate_keys(bits_input)
# sample_ciphertext = encrypt(message_input, sample_public_key)
# print("Encrypted message:", sample_ciphertext)
# sample_decrypted_message = decrypt(sample_ciphertext, sample_private_key)
# print("Decrypted message:", sample_decrypted_message)
