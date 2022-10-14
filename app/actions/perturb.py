from datetime import timedelta
from utils.util import error, find_nodes, get_date
from utils.crypto import bounded_random

expected_params = ['min', 'max']
date_format = "%Y-%m-%d"

def perturb(real_value, noise_range, is_date=False):
    noise = bounded_random(noise_range[0], noise_range[1])
    print(f'NOISE={noise}')
    if not is_date:
        return real_value + noise
    return (real_value + timedelta(days=noise)).strftime(date_format)

def perturb_nodes(node, key, value, noise_range):
    if (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    elem = node[key][idx]
                    if type(elem) in [int, float]:
                        node[key][idx] = perturb(elem, noise_range)
                    elif get_date(elem, date_format):
                        node[key][idx] = perturb(get_date(elem, date_format), noise_range, True)
                    else:
                        error(f'{type(node[key][idx])} is not a number')
        else:
            elem = node[key]
            if type(elem) in [int, float]:
                node[key] = perturb(elem, noise_range)
            elif get_date(elem, date_format):
                node[key] = perturb(get_date(elem, date_format), noise_range, True)
            else:
                error(f'{type(node[key])} is not a number')

def perturb_by_path(resource, el, params): # ONLY FOR NUMBERS AND DATES
    if not all(param in params for param in expected_params):
        error(f'Missing params (expected {expected_params})')
    ret = resource
    path = el['path']
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    perturb_nodes(ret, path[-1], el['value'], [params[elem] for elem in expected_params])