import requests
import json
from DmrIdModel import DmrIdModel
from dataclass_wizard import fromlist

# Uncomment if logger required
# requests.packages.urllib3.add_stderr_logger()

# radioid url 
url = "https://radioid.net/api/dmr/user/"

# Returned type: list of objects
def getDmrIdItems(countries: list[str]):
    if not countries:
        print('Try to get all contacts batch')
        return getDmrIdsBatch()
    else:
        return getDmrIdsPaginated(countries)


# Using '%' wildcard for 'country' to bypass pagination and fetch all records
def getDmrIdsBatch():
    query_params = {'country': '%'}
    response = requests.get(url, params=query_params)
    response_json = response.json()
    print(f'IDs count: {response_json["count"]}')
    return fromlist(DmrIdModel, response_json["results"])

def getDmrIdsPaginated(countries: list[str]):
    all_results = []
    current_page = 1
    
    while True:
        print(f'Fetching page {current_page}...')
        query_params = {'country': countries, 'page': current_page}
        response = requests.get(url, params=query_params)
        
        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            break
            
        data = response.json()
        all_results.extend(data["results"])
        
        if current_page >= data.get("pages", 1):
            break
            
        current_page += 1
        print(f'Next page {current_page} of {data["pages"]}')
    return fromlist(DmrIdModel, all_results)
 
