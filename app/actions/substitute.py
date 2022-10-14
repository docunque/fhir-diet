from utils.util import error, find_nodes

expected_params = ['substitute_with']

def substitute(old_value, new_value):
    return new_value

def substitute_nodes(node, key, value, new_value):
    if isinstance(node, list):
        [ substitute_nodes(node[node_elem_idx], key, value, new_value) for node_elem_idx in range(len(node)) ]
    elif (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    if type(node[key][idx]) == type(new_value):
                        node[key][idx] = substitute(node[key][idx], new_value)
                    else:
                        error(f'Types do not match ({type(node[key][idx])},{type(new_value)})')
        else:
            if type(node[key]) == type(new_value):
                node[key] = substitute(node[key], new_value)
            else:
                error(f'Types do not match ({type(node[key])},{type(new_value)})')

def substitute_by_path(resource, el, params):
    if not all(param in params  for param in expected_params):
        error(f'Missing params (expected {expected_params})')
    ret = resource
    path = el['path'] # "Patient.name"
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    substitute_nodes(ret, path[-1], el['value'], params[expected_params[0]])