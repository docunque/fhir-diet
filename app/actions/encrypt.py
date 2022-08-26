from Crypto.Cipher import AES
from util import error, find_nodes
import json

expected_params = ['key', 'nonce']

def encrypt(plaintext, key, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return { 'ciphertext': ciphertext, 'tag': tag }

def encrypt_nodes(node, key, value, enc_key, nonce):
    if (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    if isinstance(node[key][idx], dict):
                        node_str = json.dumps(node[key][idx])
                    else:
                        node_str = node[key][idx]
                    node[key][idx] = encrypt(node_str.encode(), enc_key, nonce)
        else:
            if isinstance(node[key], dict):
                node_str = json.dumps(node[key])
            else:
                node_str = node[key]
            node[key] = encrypt(node_str.encode(), enc_key, nonce)

def encrypt_by_path(resource, el, params):
    if not all(param in params  for param in expected_params):
        error(f'Missing params (expected {expected_params})')
    ret = resource
    path = el['path'] # "Patient.name"
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    encrypt_nodes(ret, path[-1], el['value'], params['key'], params['nonce'])