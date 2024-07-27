import csv
import re
import os.path
from radioid import getDmrIds
from transliterate import translit, get_available_language_codes
from datetime import datetime

K2_CALLSIGNS_FILE = 'k2_call_signs.csv'

# Get ids for ukraine, add more countries if required
DMR_COUNTRIES_FILTER = ['ukraine']

# Check if string contains ciryllic symbols
def hasCiryllic(string):
    return bool(re.search('[а-яА-Я]', string))

# Concatenate firstName+surName, transliterate if has ciryllic symbols
def parseName(contact):
    name = contact["fname"].strip() + ' ' + contact["surname"].strip()
    if hasCiryllic(name):
        print("Callsign %s has ciryllic in name: [%s]" % (contact["callsign"], name))
        name = translit(name, "uk", reversed=True)
        print("Transliterated as [%s]" % name)
    return name

# Get k2 callsigns as dictionary
def getK2Callsigns():
    if os.path.isfile(K2_CALLSIGNS_FILE):
        with open(K2_CALLSIGNS_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            callsigns = list(filter(lambda row: row["DMR_ID"] != "null", list(reader)))
            dictionary = {row["DMR_ID"] : row["K2CallSign"] for row in callsigns}
            return dictionary
    else:
        print("%s not found, skip" % K2_CALLSIGNS_FILE)

k2 = getK2Callsigns()

def findK2CallSign(contact):
    if k2 is None:
        return None
    dmrid = str(contact["id"])
    k2CallSign = k2.get(dmrid)
    if k2CallSign is not None:
        k2CallSign = translit(k2CallSign, "uk", reversed=True) if hasCiryllic(k2CallSign) else k2CallSign
        print("DMR_ID %s has k2CallSign %s" % (dmrid, k2CallSign))
        return k2CallSign

# headers
headers = ["No.", "TG/DMR ID", "Call Alert", "Name", "City", "Call Type", "Callsign", "State/Prov", "Country", "Remarks"]

file_name = datetime.now().strftime("%Y%m%d-%H%M%S-") + "anytone-contacts" + ".csv"

csv_file = open(file_name, 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(headers)

contacts = getDmrIds(DMR_COUNTRIES_FILTER)

count = 1
for contact in contacts:
    k2CallSign = findK2CallSign(contact)
    name = parseName(contact) if k2CallSign is None else "K2-" + k2CallSign

    row = [
        count,
        contact["id"],
        "None",
        name,
        contact["city"],
        "",
        contact["callsign"],
        contact["state"],
        contact["country"],
        ""]
    csv_writer.writerow(row)
    count += 1
csv_file.close()

print("Saved to file: ", file_name)
