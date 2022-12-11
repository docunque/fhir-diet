from utils.util import not_implemented
from actions.keep import keep_by_path
from actions.redact import redact_by_path
from actions.cryptohash import cryptohash_by_path
from actions.perturb import perturb_by_path
from actions.substitute import substitute_by_path

actions = {
    "keep": keep_by_path,
    "redact": redact_by_path,
    "perturb": perturb_by_path,
    "cryptohash": cryptohash_by_path,
    "substitute": substitute_by_path
}


def perform_deidentification(action, resource, el, params):
    if action in list(actions.keys()):
        actions[action](resource, el, params)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource
