import fhirpathpy
from utils.util import not_implemented
from actions.ttp import list_by_path, pseudonymize_by_path, depseudonymize_by_path

pseudo_actions = {
    "ttp_gen_list": list_by_path,
    "ttp_pseudonymize": pseudonymize_by_path
}

depseudo_actions = {
    "ttp_depseudonymize": depseudonymize_by_path
}


def perform_ttp_pseudonymization(action, resource, el, params):
    if action in list(pseudo_actions.keys()):
        # print(f'RES={resource}\nEL={el}\nPARAMS={params}')
        pseudo_actions[action](resource, el, params)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource


def perform_ttp_depseudonymization(action, resource, el, params):
    if action in list(depseudo_actions.keys()):
        # print(f'RES={resource}\nEL={el}\nPARAMS={params}')
        depseudo_actions[action](resource, el, params)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource