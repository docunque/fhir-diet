from utils.util import error, find_nodes
from utils.crypto import rsa_encrypt
import json

supported_enc_schemes = {
    'RSA': rsa_encrypt
}
expected_params = { 'RSA': [ 'public_key' ] }
encoding = 'utf-8'

def _encrypt(plaintext, enc_params):
    ciphertext = supported_enc_schemes[enc_params['algorithm']](plaintext, enc_params)
    return ciphertext.hex()

def _encrypt_nodes(node, key, value, enc_params):
    if (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    if isinstance(node[key][idx], dict):
                        node_str = json.dumps(node[key][idx])
                    else:
                        node_str = node[key][idx]
                    node[key][idx] = _encrypt(node_str.encode(encoding), enc_params)
        else:
            if isinstance(node[key], dict):
                node_str = json.dumps(node[key])
            else:
                node_str = node[key]
            node[key] = _encrypt(node_str.encode(encoding), enc_params)

def encrypt_by_path(resource, el, params):
    if not all(param in params for param in expected_params[params['algorithm']]):
        error(f'Missing params (expected {expected_params[params["algorithm"]]})')
    ret = resource
    path = el['path']
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    _encrypt_nodes(ret, path[-1], el['value'], params)