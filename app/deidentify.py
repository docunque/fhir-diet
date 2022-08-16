from fhirpathpy import evaluate


def perform_deidentification(resource, settings):
    for rule in settings.rules:
        result = evaluate(resource, rule, [])
        print(result)
    return {'test': 123, 'rules': settings.rules}
