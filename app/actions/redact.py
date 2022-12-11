from utils.util import find_nodes

def _del_nodes(node, key, value):
    if isinstance(node, list):
        [_del_nodes(node[node_elem_idx], key, value)
         for node_elem_idx in range(len(node))]
    elif (key in list(node.keys())):
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    del node[key][idx]
                if len(node[key]) == 0:
                    del node[key]
        else:
            del node[key]


def redact_by_path(resource, el, params):
    ret = resource
    path = el['path']  # "Patient.name"
    path = path.split('.')[1:]  # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    _del_nodes(ret, path[-1], el['value'])