import fhirpathpy
from utils.util import not_implemented
from actions.decrypt import decrypt_by_path

actions = {
    "decrypt": decrypt_by_path,
}

def perform_depseudonymization(action, resource, el, params):
    # for rule in settings.rules:
    #     fhirpathpy.engine.invocations['log'] = {'fn': lambda ctx, els: [{'path': x.path, 'value': x.data} for x in els]}
    #     matched_elements = fhirpathpy.evaluate(resource, rule['match'] + '.log()', [])
    #     for el in matched_elements:
    #         action = rule['action']
    if action in list(actions.keys()):
        actions[action](resource, el, params)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource
