from importlib import import_module
from cli import read_file
import pydoc

package_module = "fhir.resources"
header = "Python Library Documentation: package fhir.resources in fhir\n\nN\x08NA\x08AM\x08ME\x08E\n    fhir.resources - # -*- coding: utf-8 -*-\n\nP\x08PA\x08AC\x08CK\x08KA\x08AG\x08GE\x08E \x08 C\x08CO\x08ON\x08NT\x08TE\x08EN\x08NT\x08TS\x08S\n    DSTU2 (package)\n    STU3 (package)\n    "
footer = "\n\nF\x08FU\x08UN\x08NC\x08CT\x08TI\x08IO\x08ON\x08NS\x08S\n    c\x08co\x08on\x08ns\x08st\x08tr\x08ru\x08uc\x08ct\x08t_\x08_f\x08fh\x08hi\x08ir\x08r_\x08_e\x08el\x08le\x08em\x08me\x08en\x08nt\x08t(element_type: str, data: Union[Dict[str, Any], str, bytes, pathlib.Path]) -> fhir.resources.core.fhirabstractmodel.FHIRAbstractModel\n    \n    g\x08ge\x08et\x08t_\x08_f\x08fh\x08hi\x08ir\x08r_\x08_m\x08mo\x08od\x08de\x08el\x08l_\x08_c\x08cl\x08la\x08as\x08ss\x08s(model_name: str) -> Type[fhir.resources.core.fhirabstractmodel.FHIRAbstractModel]\n\nD\x08DA\x08AT\x08TA\x08A\n    _\x08__\x08_a\x08al\x08ll\x08l_\x08__\x08_ = ['get_fhir_model_class', 'construct_fhir_element']\n    _\x08__\x08_f\x08fh\x08hi\x08ir\x08r_\x08_v\x08ve\x08er\x08rs\x08si\x08io\x08on\x08n_\x08__\x08_ = '4.0.1'\n\nV\x08VE\x08ER\x08RS\x08SI\x08IO\x08ON\x08N\n    6.4.0\n\nF\x08FI\x08IL\x08LE\x08E\n    /Users/serse/Library/Python/3.8/lib/python/site-packages/fhir/resources/__init__.py\n\n"
delimiter = "\n    "
exclusions = ["(package)"]

classes = pydoc.render_doc(package_module).split(header)[1].split(footer)[0].split(delimiter)

filtered_classes = [c for c in classes for ex in exclusions if ex not in c]


resource = read_file('test/fhir/simple_patient.json')
type = resource["resourceType"]
print ('TYPE:', type)
res = "fhir.resources"
modul = "fhir.resources.%s" %(type.lower())
print ('MODULE: ', modul)

# from fhir.resources.patient import Patient
# obj = Patient.parse_obj(resource)
# print(obj.json())

#exit()


try:
    module = import_module(modul)
    my_class = getattr(module, type)
except ImportError:
    print('ERROR')


obj = my_class.parse_obj(resource)
print(obj.name[0].json())