from util import error, find_nodes

expected_params = ['noise']

def perturb(real_value, noise):
    return real_value + noise

def perturb_nodes(node, key, value, noise):
    if (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    if type(node[key][idx]) in [int, float]:
                        node[key][idx] = perturb(node[key][idx], noise)
                    else:
                        error(f'{type(node[key][idx])} is not a number')
        else:
            if type(node[key]) in [int, float]:
                node[key] = perturb(node[key], noise)
            else:
                error(f'{type(node[key])} is not a number')

def perturb_by_path(resource, el, params): # ONLY FOR NUMBERS
    if not all(param in params  for param in expected_params):
        error(f'Missing params (expected {expected_params})')
    ret = resource
    path = el['path']
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    perturb_nodes(ret, path[-1], el['value'], params[expected_params[0]])