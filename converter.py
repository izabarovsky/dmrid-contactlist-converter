import requests
import csv
import logging
from datetime import datetime

# Uncomment if logger required
# requests.packages.urllib3.add_stderr_logger()

# radioid url 
url = "https://radioid.net/api/dmr/user/"
# hardcoded filter, change it if need
query_params = {'country': 'ukraine'}
# headers
headers = ["No.", "TG/DMR ID", "Call Alert", "Name", "City", "Call Type", "Callsign", "State/Prov", "Country", "Remarks"]

response = requests.get(url, params=query_params)
response_json = response.json()

print("Total:", response_json["count"])

file_name = datetime.now().strftime("%Y%m%d-%H%M%S-") + "anytone-contacts" + ".csv"

contacts = response_json["results"]
csv_file = open(file_name, 'w')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(headers)
count = 1
for contact in contacts:
    print(contact)
    row = [count, contact["id"], "None", contact["fname"] + contact["surname"], contact["city"], "", contact["callsign"], contact["state"], contact["country"], ""]
    csv_writer.writerow(row)
    count += 1
csv_file.close()

print("Saved to file: ", file_name)

