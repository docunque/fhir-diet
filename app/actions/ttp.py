from utils.util import error, find_nodes
from actions.substitute import _substitute_nodes
import csv

expected_params = ['output_file', 'mapping_file', 'separator', 'header_lines']


def _find_pseudonym(mapping_file, separator=',', header_lines=0, value='', reverse=False):
    with (open(mapping_file, 'r')) as fin:
        reader = csv.reader(fin, delimiter=separator)
        rows = [row for row in reader]
        mappings = dict((row[0], row[1]) for row in rows[header_lines:])
    if reverse:
        key_value = {i for i in mappings if mappings[i] == value}
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
    separator = params[expected_params[2]
                       ] if expected_params[2] in params else ','
    header_lines = params[expected_params[3]
                          ] if expected_params[3] in params else 0
    pseudonym = _find_pseudonym(
        params[expected_params[1]], separator, header_lines, el['value'])
    _substitute_nodes(ret, path[-1], el['value'], pseudonym)


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
    separator = params[expected_params[2]
                       ] if expected_params[2] in params else ','
    header_lines = params[expected_params[3]
                          ] if expected_params[3] in params else 0

    depseudonym = _find_pseudonym(
        params[expected_params[1]], separator, header_lines, el['value'], True)
    _substitute_nodes(ret, path[-1], el['value'], depseudonym)
