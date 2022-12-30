# FHIR-Diet

## What is it about?

FHIR-Diet is a _HL7 FHIR de-identification tool_ written in python.
The tool has been developed by [Docunque](https://www.docunque.it) for the [HOSMARTAI](https://www.hosmartai.eu/) open call.

![logo_project](https://user-images.githubusercontent.com/696267/181810750-a57d706b-92d0-4a2f-a9d9-b39f781858d9.jpg)

## How does it work?

The tool accept a FHIR resource as _input_, and output a de-identified or pseudonymized resource as _output_.
The resource is treated according to the rules written in a _configuration file_.
In such file, the rules are expressed using a match-action principle.
The _matches_ are expressed using [FHIR Path](https://build.fhir.org/ig/HL7/FHIRPath/).
The _actions_ can be such redact, cryptohash or the other documented in this file.

![architecture](https://user-images.githubusercontent.com/696267/210065661-71900285-0d99-4ddc-b12b-430145ebd721.png)
 logo architecture

For instance, to implement "remove patient's name" it sufficies to create a configuration file like this:

```yaml
general:
  appname: FHIR-DIET
rules:
  - match: Patient.name
    action: redact
```

## Installing the system

Installing the system is straightforward. Clone this git repository and install the requirements.

```sh
git clone https://github.com/docunque/fhir-diet.git
pip install -r requirements.txt
```


## Running the system
The service is provided either through a Command Line Interface (CLI) or through a web service. You can also choose to run the system using Docker.
### Web service

To run the FHIR-Diet as web service:

```sh
cd app
uvicorn main:app --reload
```

then open the [this link](http://127.0.0.1:8000) or [that link](http://127.0.0.1:8000/redoc) to browse the API.
It is now possible to send a resource to the service in a POST request body, through the `/process` endpoint. You can try it using the [swagger API](http://127.0.0.1:8000).

### Docker

To run the web service as Docker:

```sh
docker build . -t fhir-diet
docker run -p 8000:80 fhir-diet
```

### Command Line Interface

To run the FHIR-Diet as CLI you should run `cli.py` using this syntax:

```
Usage: cli.py [OPTIONS] RESOURCE_FILENAME [CONFIG_FILENAME]
```

For example:

```sh
python3 cli.py test/fhir/simple_patient.json test/config/safe_harbor_redact.yaml
```

## Unit Tests
You can run some test cases in this way:

```sh
cd app
python3 -m unittest test.test_deidentify
python3 -m unittest test.test_pseudonymize
python3 -m unittest test.test_processor
```

## Supported actions

### De-identification actions

| Action                                                                                               | Description                                                                                                      |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `cryptohash` | Use a hash function on the element selected by the FHIR-path query. We implemented SHA3 256 as state of the art. |
| `perturb` | Change a numerical value introducing a random positive or negative value. We implemented the method for integer, float and date, allowing to introduce a random number of days |
| `redact` | Remove the element.                                                                                              |
| `substitute`  | Substitute the element with a fixed string, e.g., "ANON"                                                         |


### Pseudonymization actions

| Action | Description
| ----------------- | ----------------------------------------- |
| `encrypt`	| Use encryption to encrypt a field identified with FHIR-Path. If the field is complex (e.g., a nested structure or a list), it is converted in JSON and then encrypted. By default we use RSA albeit the encryption scheme is configurable. | 
| `ttp_gen_list`	| Generate a csv with a list of data to be pseudonymized. |
| `ttp_pseudonymize` |	Substitute a field with its pseudonym, read by the mapping file (specified in the params with the separator and the header_lines) |



### De-pseudonymization actions
| Action| Description
| -------------------------- | ------------------------------------------- |
| `decrypt` | Decrypt a previously encrypted field. |
| `ttp_depseudonymize`	| Revert a pseudonymization using a mapping file to restore the real values of the field. |


### Other actions
| Action                                                                                               | Description
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `keep` | 	keep the element as is.  |

### Acknoledgment

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101016834.

![LOGO BLACK](https://user-images.githubusercontent.com/696267/186619641-a28b2b04-087d-4a31-a5ab-1737333220b6.png)

© Copyright HL7® logo, FHIR® logo and the flaming fire are registered trademarks owned by [Health Level Seven International](https://www.hl7.org/legal/trademarks.cfm)

"FHIR® is the registered trademark of HL7 and is used with the permission of HL7. Use of the FHIR trademark does not constitute endorsement of this product by HL7"
