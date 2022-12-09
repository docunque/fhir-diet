import fhirpathpy
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

def perform_deidentification(resource, settings):
    #if isinstance(resource, list):
    #    pass
    for rule in settings.rules:
        fhirpathpy.engine.invocations['log'] = {'fn': lambda ctx, els: [{'path': x.path, 'value': x.data} for x in els]}
        matched_elements = fhirpathpy.evaluate(resource, rule['match'] + '.log()', [])
        for el in matched_elements:
            action = rule['action']
            params = rule['params'] if 'params' in rule.keys() else {}
            if action in list(actions.keys()):
                #print(f'RES={resource}\nEL={el}\nPARAMS={params}')
                actions[action](resource, el, params)
            else:
                not_implemented(f'Method {action} is not implemented')
    return resource
