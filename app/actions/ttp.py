from utils.util import error, find_nodes
from actions.substitute import substitute_nodes
import csv

expected_params = ['output_file', 'mapping_file']


def find_pseudonym(mapping_file, value, reverse=False):
    with(open(mapping_file, 'r')) as fin:
        reader = csv.reader(fin)
        mappings = dict((row[0], row[1]) for row in reader)
    if reverse:
        key_value = { i for i in mappings if mappings[i] == value }
        return key_value.pop()
    return mappings[value]


def list_by_path(resource, el, params):
    outfile = params[expected_params[0]
                     ] if expected_params[0] in params else './list.csv'
    with (open(outfile, 'a+')) as fin:
        fin.write(f"{str(el['value'])}\n")


def pseudonymize_by_path(resource, el, params):
    if expected_params[1] not in params:
        error(f'Missing params (expected {expected_params[1]})')
    ret = resource
    path = el['path']  # "Patient.name"
    path = path.split('.')[1:]  # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    pseudonym = find_pseudonym(params[expected_params[1]], el['value'])
    substitute_nodes(ret, path[-1], el['value'], pseudonym)


def depseudonymize_by_path(resource, el, params):
    if expected_params[1] not in params:
        error(f'Missing params (expected {expected_params[1]})')
    ret = resource
    path = el['path']  # "Patient.name"
    path = path.split('.')[1:]  # Remove root
    if len(path) == 0:
        ret.clear()
        return
    ret = find_nodes(ret, path[:-1], [])
    depseudonym = find_pseudonym(params[expected_params[1]], el['value'], True)
    substitute_nodes(ret, path[-1], el['value'], depseudonym)
