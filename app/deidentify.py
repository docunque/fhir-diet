import fhirpathpy
from hashlib import sha3_256

# tokens = ['where', 'first()']
# where_values = { 'position': 'pos'}

# tokens = [ { 'where': { 'key': 'key', 'value': 'value' } }, { 'first()': { 'pos': 0 } }, ]

# def get_wheres(math_str):
#     match_split = math_str.split('.')
#     wheres = []
#     for segment in match_split:
#         print(f'Segment {segment}')
#         for tid, token in enumerate(tokens):
#             print(f'Token {token}')
#             key = list(token.keys())[0]
#             if key in segment:
#                 print(f'Found {token}')
#                 if tid == 0:
#                     where_dict = segment.split(key+'(')[1].split(')')[0].split('=')
#                     print(f'WhereDICT {where_dict}')
#                     if len(where_dict) != 2:
#                         raise Exception
#                     else:
#                         key_str = where_dict[0]
#                         value_str = where_dict[1][1:-1] if ("'" in where_dict[1]) else where_dict[1]
#                         print(f'Key {key_str}\tValue {value_str}')
#                         wheres.append({key_str: value_str})
#                 if tid == 1:
#                     wheres.append(token[key])
#     return wheres


def find_nodes(node, path_list, wheres):
    if len(path_list) == 0:
        return node
    if isinstance(node, list):
        return [find_nodes(item, path_list, wheres) for item in node]
    if isinstance(node, dict):
        key = path_list[0]
        if key in list(node.keys()):
            del path_list[0]
            return find_nodes(node[key], path_list, wheres)
        else:
            raise Exception

def del_nodes(node, key, value):
    if (key in list(node.keys())):
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

def del_by_path(resource, el):
    ret = resource
    path = el['path'] # "Patient.name"
    path = path.split('.')[1:] # Remove root
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
    
def set_nodes(node, key, value, new_value):
    if (key in list(node.keys())):
        #print(f'Found {key} in {node}')
        if isinstance(node[key], list):
            for idx, data in enumerate(node[key]):
                if data == value:
                    node[key][idx] = new_value
        else:
            node[key] = new_value

def hash_by_path(resource, el):
    ret = resource
    path = el['path'] # "Patient.name"
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    hash_str = sha3_256(ret[path[-1]].encode()).hexdigest()
    set_nodes(ret, path[-1], el['value'], hash_str)

def get_by_path(resource, el):
    ret = resource
    path = el['path'] # "Patient.name"
    for segment in path.split('.')[1:]:
        if isinstance(ret, dict):
            ret = ret.get(segment)
        elif isinstance(ret, list):
            for idx, data in enumerate(ret):
                if data == el['data']:
                    ret = ret[idx]
    return ret


def perform_deidentification(resource, settings):
    for rule in settings.rules:
        fhirpathpy.engine.invocations['log'] = {'fn': lambda ctx, els: [{'path': x.path, 'value': x.data} for x in els]}
        matched_elements = fhirpathpy.evaluate(resource, rule['match'] + '.log()', [])
        for el in matched_elements:
            if rule['action'] == 'redact':
                del_by_path(resource, el)
            elif rule['action'] == 'cryptoHash':
                hash_by_path(resource, el)
            else:
                raise NotImplemented(f'Method {rule["action"]} is not implemented')
    return resource
