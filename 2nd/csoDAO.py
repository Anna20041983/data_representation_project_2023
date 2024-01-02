import requests
import json


#url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/SCA05/JSON-stat/2.0/en"
#url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/SCA06/JSON-stat/2.0/en"
urlBeginning = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
urlEnd = "/JSON-stat/2.0/en"

class CsoDao:
    def getAllAsFile(self, dataset, filename):
        data = self.getAll(dataset)
        with open(filename, "wt") as fp:
            print(json.dumps(data), file=fp)

    def getAll(self, dataset):
        url = urlBeginning + dataset + urlEnd
        response = requests.get(url)
        return response.json()

    def getFormattedAsFile(self, dataset, filename):
        formatted_data = self.getFormatted(dataset)
        with open(filename, "wt") as fp:
            print(json.dumps(formatted_data), file=fp)

    def getFormatted(self, dataset):
        data = self.getAll(dataset)
        ids = data["id"]
        values = data["value"]
        dimensions = data["dimension"]
        sizes = data["size"]
        valueCount = 0
        result = {}

        for dim0 in range(0, sizes[0]):
            currentId = ids[0]
            index = dimensions[currentId]["category"]["index"][dim0]
            label0 = dimensions[currentId]["category"]["label"][index]
            result[label0] = {}

            for dim1 in range(0, sizes[1]):
                currentId = ids[1]
                index = dimensions[currentId]["category"]["index"][dim1]
                label1 = dimensions[currentId]["category"]["label"][index]
                result[label0][label1] = {}

                for dim2 in range(0, sizes[2]):
                    currentId = ids[2]
                    index = dimensions[currentId]["category"]["index"][dim2]
                    label2 = dimensions[currentId]["category"]["label"][index]
                    result[label0][label1][label2] = {}

                    for dim3 in range(0, sizes[3]):
                        currentId = ids[3]
                        index = dimensions[currentId]["category"]["index"][dim3]
                        label3 = dimensions[currentId]["category"]["label"][index]
                        result[label0][label1][label2][label3] = {}

                        for dim4 in range(0, sizes[4]):
                            currentId = ids[4]
                            index = dimensions[currentId]["category"]["index"][dim4]
                            label4 = dimensions[currentId]["category"]["label"][index]
                            result[label0][label1][label2][label3][label4] = {}

                            for dim5 in range(0, sizes[5]):
                                currentId = ids[5]
                                index = dimensions[currentId]["category"]["index"][dim5]
                                label5 = dimensions[currentId]["category"]["label"][index]
                                result[label0][label1][label2][label3][label4][label5]  = values[valueCount]
                                db_values = (label1, label2, label3, label4, label5, values[valueCount])
         
                                valueCount += 1

        return result



if __name__ == "__main__":
    datasets = ["SCA06", "SCA05"]
    
    csoDAO = CsoDao()
    
    for dataset in datasets:
        filename = f"{dataset.lower()}_formatted.json"
        csoDAO.get_formatted_as_file(dataset, filename)
