#!python.exe

import hashlib
import os

#print(hashlib.algorithms_available)
#print(hashlib.algorithms_guaranteed)
""" message = hashlib.sha256()
message.update(b'pawssword')
print(message.digest())  digest = pokazi mi hash
message.update(b'1234qwer')
print(message.digest())
print('')
print('---')
print(message.hexdigest())
message.update(b'1234qwer')
print(message.hexdigest())

 """

""" def hash_string_object(input):
    byte_input = input.encode('utf-8')
    hash = hashlib.sha256(byte_input)
    return hash

def hash_string_binary(input):
    byte_input = input.encode('utf-8')
    hash = hashlib.sha256(byte_input)
    return hash.digest()

def hash_string_hex(input):
    byte_input = input.encode('utf-8')
    hash = hashlib.sha256(byte_input)
    return hash.hexdigest()

def update_hash(hash_to_update,input):
    hash_to_update.update(input.encode('utf-8'))


hash1 = hash_string_binary('1234qwer')
#hash2 =  update_hash(hash1, '1234qwer')
hash3 = hash_string_binary('1234qwer')
print(hash1 == hash3)
 """

def hash_password(password):
    password_bin = password.encode('utf-8')
    salt = os.urandom(32)
    hash = hashlib.pbkdf2_hmac(
        'sha256', password_bin, salt, 100000
    )
    return salt + hash
    

hash1 = hash_password('1234')
hash2 = hash_password('12341234qwer')
#print(hash1==hash2)

#users = {}

#hash_user1 = hash_password('1234qwer')
#users['user1'] = hash_user1

#hash_user2 = hash_password('1234qwer')
#users['user2'] = hash_password('1234qwer')
#print(hash_user1 == hash_user2)

def verify_password(password_plain_text, stored_password_hash):
    salt = stored_password_hash[:32]
    key = stored_password_hash[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', password_plain_text.encode('utf-8'), salt, 100000)
    return (key == new_hash)

#print(verify_password('1234', hash1))
#print(verify_password('12341234qwer', hash2))


