import requests

# Uncomment if logger required
# requests.packages.urllib3.add_stderr_logger()

# radioid url 
url = "https://radioid.net/api/dmr/user/"

def getDmrIds(countries: list[str]):
    query_params = {'country': countries}
    response = requests.get(url, params=query_params)
    response_json = response.json()
    print("IDs, founded in radioid:", response_json["count"])
    return response_json["results"]
