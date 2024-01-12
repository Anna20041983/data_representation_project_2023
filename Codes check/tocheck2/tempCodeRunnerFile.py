def processDimension(data, ids, dimensions, sizes, level):
    if level < len(ids):
        currentId = ids[level]
        result = {}
        for dim in range(0, sizes[level]):
            index = dimensions[currentId]["category"]["index"][dim]
            label = dimensions[currentId]["category"]["label"][index]
            result[label] = processDimension(data, ids, dimensions, sizes, level + 1) if level < 5 else data["value"][dim]
        return result
    else:
        return None  # or handle this c

def getFormatted(dataset):
    data = getAll(dataset)
    ids = data["id"]
    dimensions = data["dimension"]
    sizes = data["size"]
    return processDimension(data, ids, dimensions, sizes, 0)
