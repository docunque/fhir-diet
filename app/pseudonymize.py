import fhirpathpy
from utils.util import not_implemented
from actions.encrypt import encrypt_by_path
#from actions.ttp import ttp_by_path
from ttp_pseudonymizer import pseudo_actions as ttp_pseudo_actions, perform_ttp_pseudonymization

actions = ttp_pseudo_actions | {
    "encrypt": encrypt_by_path,
#    "ttp": ttp_by_path,
}

def perform_pseudonymization(action, resource, el, params):
    # for rule in settings.rules:
    #     fhirpathpy.engine.invocations['log'] = {'fn': lambda ctx, els: [{'path': x.path, 'value': x.data} for x in els]}
    #     matched_elements = fhirpathpy.evaluate(resource, rule['match'] + '.log()', [])
    #     for el in matched_elements:
    #         action = rule['action']
    #         params = rule['params'] if 'params' in rule.keys() else {}
    if action in list(actions.keys()):
        #print(f'RES={resource}\nEL={el}\nPARAMS={params}')
        actions[action](resource, el, params)
        #print(f'NEW RES={resource}')
    elif action in list(ttp_pseudo_actions.keys()):  # TTP (gPAS)
        perform_ttp_pseudonymization(action, resource, el, params)
    else:
        not_implemented(f'Method {action} is not implemented')
    return resource
