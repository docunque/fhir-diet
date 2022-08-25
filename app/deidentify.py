import fhirpathpy




def del_by_path(resource, el):
    ret = resource
    path = el['path'] # "Patient.name"
    for segment in path.split('.')[1:]:
        if isinstance(ret, dict):
            ret = ret.get(segment)
        elif isinstance(ret, list):
            for idx, data in enumerate(ret):
                if data == el['data']:
                    ret = ret[idx]
    print(f"deleting {ret}")
    del ret


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
                print("Deleted object")
                print(resource)
            else:
                raise NotImplemented(f'Method {rule["action"]} is not implemented')
        print(f'res: ', matched_elements)
    return {'test': 123, 'rules': settings.rules}
