from datetime import datetime
import json
import os
import sys
from rich import print

def not_implemented(msg):
    raise NotImplementedError(msg)

def error(msg):
    raise Exception(msg)

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

def get_date(date_str, date_format):
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None


def read_resource_from_file(filename: str):
    """
    Read a fhir resource from file and return the json data
    """
    try:
        with open(filename, 'r') as jfile:
            json_data = json.load(jfile)
            print(f":thumbs_up: json {filename} read")
            return json_data
    except IOError as e:
        print(
            f":sad_but_relieved_face: File {filename} does not exist.")
        print(e)
        sys.exit(os.EX_OSFILE)
    except ValueError as e:
        print(
            f":sad_but_relieved_face: Cannot parse json data.")
        print(e)
        sys.exit(os.EX_OSFILE)




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

# def get_by_path(resource, el):
#     ret = resource
#     path = el['path'] # "Patient.name"
#     for segment in path.split('.')[1:]:
#         if isinstance(ret, dict):
#             ret = ret.get(segment)
#         elif isinstance(ret, list):
#             for idx, data in enumerate(ret):
#                 if data == el['data']:
#                     ret = ret[idx]
#     return ret