import hmac
import hashlib
import secrets
import random
import statistics
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import time

shared_key = ""

def key_setup():
    shared_key = secrets.token_bytes(16)
    infile = open("shared_key.txt", "wb")
    infile.write(shared_key)
    infile.close()
    return shared_key

def random_message_gen():
    return ''.join([chr(random.randint(0, 255)) for i in range(18)])
    pass

def hash_message(message):
    hash = hashlib.sha256(message.encode()).digest()
    return hash[:1]

def find_collision(repeats):
    trial_counter = []
    for x in range(repeats):
        hash_to_message = {}
        trials = 0
        while True:
            message = random_message_gen()
            hash_value = hash_message(message)

            if hash_value in hash_to_message:
                m1 = message
                m2 = hash_to_message[hash_value]
                print("Collision found: ", m1, " and ", m2)
                print("Common hash value: ", hash_value)
                print("\n")
                trial_counter.append(trials)
                break

            hash_to_message[hash_value] = message
            trials += 1

    average_trials = statistics.mean(trial_counter)
    return average_trials


def alice_key_setup():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    file_out = open("alice_public.txt", "wb")
    file_out.write(public_key)
    file_out.close()
    return private_key

def HMAC_fun(message):
    message = message.encode()
    alice_hmac = hmac.new(shared_key, message, hashlib.sha256).digest()

    outfile = open("mactext.txt", "wb")
    outfile.write(message)
    outfile.write(alice_hmac)
    outfile.close()
    pass

def RSAsig_fun(message):
    message = message.encode()

    hash_val = SHA256.new(message)
    signature = pkcs1_15.new(RSA.import_key(alice_key)).sign(hash_val)

    file_out = open("signature.txt", "wb")
    file_out.write(message)
    file_out.write(signature)
    file_out.close()
    pass

def HMAC_timing():
    num = input("Enter how many times to run the timing test: ")
    time_sum = 0
    message = input("Enter the message: ")
    for i in range(int(num)):
        start = time.time()
        HMAC_fun(message)
        end = time.time()
        #print("Time: ", end - start)
        time_sum += end - start
        pass
    average = time_sum / int(num)
    print("Average time: ", average) 
    pass

def RSA_timing():
    num = input("Enter how many times to run the timing test: ")
    time_sum = 0
    message = input("Enter the message: ")
    for i in range(int(num)):
        start = time.time()
        RSAsig_fun(message)
        end = time.time()
        time_sum += end - start
        pass
    average = time_sum / int(num)
    print("Average time: ", average) 
    pass

def menu():
    print("Select an option:")
    print("1. Generate HMAC and save to file")
    print("2. Generate RSA signature and save to file")
    print("3. Time signature generation")
    print("4. Find average number of trials to find a collision")
    choice = input("Enter your choice: ")
    if choice == "1":
        message = input("Enter the message: ")
        HMAC_fun(message)
    elif choice == "2":
        message = input("Enter the message: ")
        RSAsig_fun(message)
    elif choice == "3":
        time_choice = input("1. HMAC timing\n2. RSA timing\nEnter your choice: ")
        if time_choice == "1":
            HMAC_timing()
        elif time_choice == "2":
            RSA_timing()
        else:
            print("Invalid choice")
            pass
        pass
    elif choice == '4':
        print("Enter number of iterations: ")
        repeats = int(input())
        average_trials = find_collision(repeats)
        print("Average number of trials to find a collision: ", average_trials)
    else:
        print("Invalid choice")

shared_key = key_setup()
alice_key = alice_key_setup()

menu()
