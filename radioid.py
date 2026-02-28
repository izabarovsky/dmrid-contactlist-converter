import requests
import json
from DmrIdModel import DmrIdModel
from dataclass_wizard import fromlist

# Uncomment if logger required
# requests.packages.urllib3.add_stderr_logger()

# radioid url 
url = "https://radioid.net/api/dmr/user/"

# Returned type: list
def getDmrIds(countries: list[str]):
    query_params = {'country': countries}
    response = requests.get(url, params=query_params)
    response_json = response.json()
    print("IDs, founded in radioid:", response_json["count"])
    return response_json["results"]


# Returned type: list of objects
def getDmrIdItems(countries: list[str]):
    query_params = {'country': countries}
    response = requests.get(url, params=query_params)
    response_json = response.json()
    print("IDs, founded in radioid:", response_json["count"])
    return fromlist(DmrIdModel, response_json["results"])

