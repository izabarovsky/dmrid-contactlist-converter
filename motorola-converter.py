import csv
import os.path
import re
from DmrIdModel import DmrIdModel
from radioid import getDmrIds, getDmrIdItems
from datetime import datetime
from transliterate import transliterate, hasCiryllic

# SETTINGS SECTION START

# Local Kyiv callsigns, skip if you don't know what is that
K2_CALLSIGNS_FILE = 'k2_call_signs.csv'
# Get ids for ukraine, add more countries if required
DMR_COUNTRIES_FILTER = ['ukraine']
# Alias max size
ALIAS_MAX_SIZE = 16
# Result filename
file_name = datetime.now().strftime("%Y%m%d-%H%M%S-") + "simple-contacts.csv"
# Additional filter by regexp, comment to disable
# FILTER_BY_PATTERN = r"^..[0-8]E.*"

# SETTINGS SECTION END


# Get k2 callsigns as dictionary
def getK2Callsigns():
    print("%s found, names should be replaced with K2 callsign" % K2_CALLSIGNS_FILE)
    if os.path.isfile(K2_CALLSIGNS_FILE):
        with open(K2_CALLSIGNS_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            callsigns = list(filter(lambda row: row["DMR_ID"] != "null", list(reader)))
            dictionary = {row["DMR_ID"] : row["K2CallSign"] for row in callsigns}
            return dictionary

k2 = getK2Callsigns()

def findK2CallSign(contact):
    if k2 is None:
        return None
    dmrid = str(contact.id)
    k2CallSign = k2.get(dmrid)
    if k2CallSign is not None:
        k2CallSign = transliterate(k2CallSign) if hasCiryllic(k2CallSign) else k2CallSign
        #print("DMR_ID %s has k2CallSign %s" % (dmrid, k2CallSign))
        return k2CallSign
    
def resolveCyrillic(contacts):
    for contact in contacts:
        for key, value in vars(contact).items():
            if not isinstance(value, str):
                continue
            if hasCiryllic(value):
                trasliteratedText = transliterate(value)
                print("%s has %s=%s, transliterated to %s" % (contact.callsign, key, value, trasliteratedText))
                setattr(contact, key, trasliteratedText)
    return contacts

def cuttingAliases(contacts):
    for contact in contacts:
        contact.alias = contact.alias[:ALIAS_MAX_SIZE - 1]
    return contacts

def resolveAliases(contacts):
    for contact in contacts:
        contact.alias = contact.callsign + " " + contact.fname
    return contacts

def resolveAliasDuplicates(contacts):
    print("Resolve aliases duplicates")
    aliases = list(map(lambda contact: contact.alias, contacts))
    duplicates = list([i for i in contacts if aliases.count(i.alias) > 1])
    
    duplicatesCallsigns = map(lambda contact: contact.callsign, duplicates)
    duplicatesCallsigns = set(duplicatesCallsigns)
    
    duplicatesMerged = dict()
    for callsign in duplicatesCallsigns:
        sameCallsignIds = [i.id for i in duplicates if i.callsign == callsign]
        print("Operator %s has ids %s" % (callsign, sameCallsignIds))
        duplicatesMerged.update({callsign: sameCallsignIds})
        
    for callsign, ids in duplicatesMerged.items():
        count = 1
        for dmrid in ids:
            contact = next(contact for contact in contacts if contact.id == dmrid )
            contact.alias = f"{callsign}-{count:02d}"
            count += 1
    return contacts

# Headers
headers = ["DMR ID", "Alias"]

csv_file = open(file_name, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(headers)

contacts = getDmrIdItems(DMR_COUNTRIES_FILTER)

try:
    if FILTER_BY_PATTERN:
        print("Try to filter by pattern [%s]" % (FILTER_BY_PATTERN))
        contactsBefore = len(contacts)
        contacts = [contact for contact in contacts if re.match(FILTER_BY_PATTERN, contact.callsign)]
        contactsAfter = len(contacts)
        print("Before filter %s, after filter %s" % (contactsBefore, contactsAfter))
except NameError:
    print("Filter pattern not defined, skipped")

contacts = resolveCyrillic(contacts)
contacts = resolveAliases(contacts)
contacts = cuttingAliases(contacts)
contacts = resolveAliasDuplicates(contacts)

for contact in contacts:
    k2CallSign = findK2CallSign(contact)
    record = [ contact.id, contact.alias ]
    csv_writer.writerow(record)
csv_file.close()

print("Saved to file: ", file_name)
