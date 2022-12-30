"""Stress test the application
"""

import os
import datetime
# CMD = "python3 cli.py test/fhir/simple_patient.json test/config/safe_harbor_redact.yaml"
CMD = "python3 cli.py test/fhir/simple_patient.json test/config/encrypt.yaml"
N_RUNS = 100
start_time = datetime.datetime.now()
for i in range(N_RUNS):
    os.system(CMD)
end_time = datetime.datetime.now()

print("Avg time for one iteration is ", (end_time-start_time).total_seconds()/(1.0*N_RUNS))
