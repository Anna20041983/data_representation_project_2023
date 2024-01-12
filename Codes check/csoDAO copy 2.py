from ast import Pass
import requests
import json
from physicalDAO import physicalDAO
#from disabilityDAO import disabilityDAO

#url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/SCA05/JSON-stat/2.0/en"
#url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/SCA06/JSON-stat/2.0/en"
urlBeginning = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
urlEnd = "/JSON-stat/2.0/en"

def getAllAsFile(dataset):
     with open("cso.json", "wt") as fp:
        print(json.dumps(getAll(dataset)), file=fp)

def getAll(dataset):
    url = urlBeginning + dataset + urlEnd
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as req_exc:
        print(f"Error during API request: {req_exc}")
        return None
    except json.JSONDecodeError as json_exc:
        print(f"Error decoding JSON response: {json_exc}")
        return None

def getFormattedAsFile(dataset):
    data = getAll(dataset)
    if data is not None:
        with open("cso-formatted.json", "wt") as fp:
            print(json.dumps(getFormatted(dataset)), file=fp)

def process_dimension(data, ids, dimensions, sizes, level):
    currentId = ids[level]
    result = {}
    for dim in range(0, sizes[level]):
        index = dimensions[currentId]["category"]["index"][dim]
        label = dimensions[currentId]["category"]["label"][index]
        result[label] = process_dimension(data, ids, dimensions, sizes, level + 1) if level < 5 else data["value"][dim]
    return result

def get_formatted(dataset):
    data = get_all(dataset)
    ids = data["id"]
    dimensions = data["dimension"]
    sizes = data["size"]
    return process_dimension(data, ids, dimensions, sizes, 0)


if __name__ == "__main__":
    #getFormattedAsFile("SCA05")
    getFormattedAsFile("SCA06")
    