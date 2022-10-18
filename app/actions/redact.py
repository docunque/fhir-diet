from utils.util import find_nodes


def del_nodes(node, key, value):
    if isinstance(node, list):
        [del_nodes(node[node_elem_idx], key, value)
         for node_elem_idx in range(len(node))]
    elif (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    #ret[path[-1]][idx] = 'ciao'
                    del node[key][idx]
                if len(node[key]) == 0:
                    del node[key]
        else:
            #ret[path[-1]] = 'bau'
            del node[key]


def redact_by_path(resource, el, params):
    ret = resource
    path = el['path']  # "Patient.name"
    path = path.split('.')[1:]  # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    #print('FIND', ret)
    # for segment in path[:-1]:
    #     if isinstance(ret, dict):
    #         ret = ret.get(segment)
    #     elif isinstance(ret, list):
    #         for idx, data in enumerate(ret):
    #             if data == el['value']:
    #                 ret = ret[idx]
    #print(f'{path[-1]} in {list(ret.keys())}')
    del_nodes(ret, path[-1], el['value'])

# def del_by_path(resource, el):
#     ret = resource
#     path = el['path'] # "Patient.name"
#     path = path.split('.', 1)[1] # Remove root
#     for segment in path.split('.'):
#         if isinstance(ret, dict):
#             ret = ret.get(segment)
#         elif isinstance(ret, list):
#             for idx, data in enumerate(ret):
#                 if data == el['value']:
#                     ret = ret[idx]
#     del ret[segment]
