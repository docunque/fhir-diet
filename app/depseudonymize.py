from utils.util import not_implemented
from actions.decrypt import decrypt_by_path
from ttp_pseudonymizer import depseudo_actions as ttp_depseudo_actions, perform_ttp_depseudonymization

actions = ttp_depseudo_actions | {
    "decrypt": decrypt_by_path,
}


def perform_depseudonymization(action, resource, el, params):
    if action in list(actions.keys()):
        actions[action](resource, el, params)
    elif action in list(ttp_depseudo_actions.keys()):  # TTP (gPAS)
        perform_ttp_depseudonymization(action, resource, el, params)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource
