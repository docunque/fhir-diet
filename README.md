# fhir-diet

HL7 FHIR de-identification tool.
This tool is currently under construction for [HOSMARTAI](https://www.hosmartai.eu/) open call.

![logo_project](https://user-images.githubusercontent.com/696267/181810750-a57d706b-92d0-4a2f-a9d9-b39f781858d9.jpg)

---

## Instruction
**Install**

```
pip install -r requirements.txt
```

**Run**

```
cd app
uvicorn main:app --reload
```

**Test**

```
python -m unittest test.test_config
```

**Docs**

```
http://localhost:8000/docs
```

**Docker**

```
docket build . -t fhir-diet
docker run -p 8000:80 fhir-diet
```
