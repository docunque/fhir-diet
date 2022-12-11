from utils.util import not_implemented
from actions.encrypt import encrypt_by_path
from ttp_pseudonymizer import pseudo_actions as ttp_pseudo_actions, perform_ttp_pseudonymization

actions = ttp_pseudo_actions | {
    "encrypt": encrypt_by_path
}

def perform_pseudonymization(action, resource, el, params):
    if action in list(actions.keys()):
        actions[action](resource, el, params)
    elif action in list(ttp_pseudo_actions.keys()):  # TTP (gPAS)
        perform_ttp_pseudonymization(action, resource, el, params)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource
