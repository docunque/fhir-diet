# fhir-diet

HL7 FHIR de-identification tool.
This tool is currently under construction for [HOSMARTAI](https://www.hosmartai.eu/) open call.

![LOGO BLACK](https://user-images.githubusercontent.com/696267/186619641-a28b2b04-087d-4a31-a5ab-1737333220b6.png)

![logo_project](https://user-images.githubusercontent.com/696267/181810750-a57d706b-92d0-4a2f-a9d9-b39f781858d9.jpg)

---

## Instruction
**Install**

```
pip install -r requirements.txt
```

**Run**

Run the web service

```
cd app
uvicorn main:app --reload
```

Run as CLI

```
python cli.py pseudonymize test/fhir/simple_patient.json
python cli.py deidentify test/fhir/simple_patient.json
```

**Test**

```
cd app
python3 -m unittest test.test_config
python3 -m unittest test.test_deidentify
python3 -m unittest test.test_cli
```

**Docs**

```
http://localhost:8000/docs
```

or

```
http://127.0.0.1:8000/redoc
```

**Docker**

```
docker build . -t fhir-diet
docker run -p 8000:80 fhir-diet
```

**Credits**
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101016834

© Copyright HL7® logo, FHIR® logo and the flaming fire are registered trademarks owned by [Health Level Seven International](https://www.hl7.org/legal/trademarks.cfm)

"FHIR® is the registered trademark of HL7 and is used with the permission of HL7. Use of the FHIR trademark does not constitute endorsement of this product by HL7"
