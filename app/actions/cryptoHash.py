from utils.util import find_nodes
from Crypto.Hash import SHA3_256
import json

def _compute_hash(msg):
    return SHA3_256.new(msg).hexdigest()

def _hash_nodes(node, key, value):
    if (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    if isinstance(node[key][idx], dict):
                        node_str = json.dumps(node[key][idx])
                    else:
                        node_str = node[key][idx]
                    node[key][idx] = _compute_hash(node_str.encode())
        else:
            if isinstance(node[key], dict):
                node_str = json.dumps(node[key])
            else:
                node_str = node[key]
            node[key] = _compute_hash(node_str.encode())

def cryptohash_by_path(resource, el, params):
    ret = resource
    path = el['path'] # "Patient.name"
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    _hash_nodes(ret, path[-1], el['value'])