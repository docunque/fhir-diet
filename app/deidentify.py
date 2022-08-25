import fhirpathpy

def del_by_path(resource, el):
    ret = resource
    path = el['path'] # "Patient.name"
    path = path.split('.')[1:] # Remove root
    if len(path) == 0:
        ret.clear()
        return
    for segment in path[:-1]:
        if isinstance(ret, dict):
            ret = ret.get(segment)
        elif isinstance(ret, list):
            for idx, data in enumerate(ret):
                if data == el['value']:
                    ret = ret[idx]
    if (path[-1] in list(ret.keys())):
        if isinstance(ret[path[-1]], list):
            for idx, data in enumerate(ret[path[-1]]):
                if data == el['value']:
                    del ret[path[-1]][idx]
                if len(ret[path[-1]]) == 0:
                    del ret[path[-1]]
        else:
            del ret[path[-1]]

# def del_by_path(resource, el):
#     ret = resource
#     path = el['path'] # "Patient.name"
#     path = path.split('.', 1)[1] # Remove root
#     for segment in path.split('.'):
#         if isinstance(ret, dict):
#             ret = ret.get(segment)
#         elif isinstance(ret, list):
#             for idx, data in enumerate(ret):
#                 if data == el['value']:
#                     ret = ret[idx]
#     del ret[segment]

def get_by_path(resource, el):
    ret = resource
    path = el['path'] # "Patient.name"
    for segment in path.split('.')[1:]:
        if isinstance(ret, dict):
            ret = ret.get(segment)
        elif isinstance(ret, list):
            for idx, data in enumerate(ret):
                if data == el['data']:
                    ret = ret[idx]
    return ret



def set_by_path(resource, path, replaced):
    pass


def perform_deidentification(resource, settings):
    for rule in settings.rules:
        fhirpathpy.engine.invocations['log'] = {'fn': lambda ctx, els: [{'path': x.path, 'value': x.data} for x in els]}
        matched_elements = fhirpathpy.evaluate(resource, rule['match'] + '.log()', [])
        for el in matched_elements:
            if rule['action'] == 'redact':
                # list of resource nodes
                del_by_path(resource, el)
                #print("Deleted object")
                #print(f"Updated resource = {resource}")
            else:
                raise NotImplemented(f'Method {rule["action"]} is not implemented')
    return resource
