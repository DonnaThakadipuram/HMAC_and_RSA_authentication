import hmac
import hashlib
import secrets
import random
import statistics
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import time

def key_setup():
    f = open("shared_key.txt", "rb")
    shared_key = f.read()
    f.close()
    return shared_key
    pass

def HMAC_fun(message_size, shared_key):

    f = open("mactext.txt", "rb")
    test_message = f.read(message_size)
    hmac_digest = f.read()
    f.close()

    calculated_hmac = hmac.new(shared_key, test_message, hashlib.sha256).digest()

    if hmac.compare_digest(calculated_hmac, hmac_digest):
        print("Derived HMAC: ", calculated_hmac.hex())
        print("Message HMAC: ", hmac_digest.hex())
        return "Message is authentic"
    
    else:
        print("Derived HMAC: ", calculated_hmac.hex())
        print("Message HMAC: ", hmac_digest.hex())
        return "Message is not authentic"
        pass
    pass

def RSA_fun(message_size):
    f = open("alice_public.txt", "rb")
    public_key = f.read()
    f.close()

    message_size = int(message_size)

    f = open("signature.txt", "rb")
    message = f.read(message_size)
    signature = f.read()
    f.close()

    hash_val = SHA256.new(message)

    try:
        pkcs1_15.new(RSA.import_key(public_key)).verify(hash_val, signature)
        return "The signature is valid."
    except (ValueError, TypeError):
        return "The signature is not valid."
    pass

def RSA_timing():
    num = input("Enter how many times to run the timing test: ")
    message_size = input("Enter the message size: ")

    time_sum = 0
    for i in range(int(num)):
        start = time.time()
        RSA_fun(message_size)
        end = time.time()
        #print("Time: ", end - start)
        time_sum += end - start
        
        pass
    print("Average time: ", time_sum / int(num))
    pass

def menu():
    print("Select an option:")
    print("1. HMAC Verification")
    print("2. RSA Verification")
    print("3. RSA Timing")
    choice = input("Enter your choice: ")
    if choice == "1":
        shared_key = key_setup()
        message_size = input("Enter the message size: ")
        print(HMAC_fun(int(message_size), shared_key))
        pass
    elif choice == "2":
        message_size = input("Enter the message size: ")
        print(RSA_fun(int(message_size)))
        
        pass
    elif choice == "3":
        RSA_timing()
        pass
menu()