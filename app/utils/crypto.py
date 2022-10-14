from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from random import randint

def bounded_random(min, max):
    return randint(min, max)

def rsa_encrypt(plaintext, enc_params):
    key_path = enc_params['public_key']
    with open(key_path) as fin:
        pub_key_data = fin.read()
    public_key = RSA.import_key(pub_key_data)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(plaintext)

def rsa_decrypt(ciphertext, dec_params):
    key_path = dec_params['private_key']
    with open(key_path) as fin:
        priv_key_data = fin.read()
    private_key = RSA.import_key(priv_key_data)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(ciphertext)

def aes_enc(plaintext, enc_params):
    key = enc_params[0]
    nonce = enc_params[1]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return { 'ciphertext': ciphertext, 'tag': tag }