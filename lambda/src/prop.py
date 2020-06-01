import math

LAMBDA_PARAM = -1 / 10

def get_weighted_average(inventory):

    X = lambda d: math.exp(LAMBDA_PARAM * d)

    weights = [0] * len(inventory)

    curr_time = inventory[-1]["timestamp"]

    for i in range(1, len(inventory) + 1):
        minute_diff = (curr_time - inventory[-i]["timestamp"]).total_seconds() / 60.0
        weights[-i] = X(minute_diff)

    wav = 0

    for i in range(1, len(inventory) + 1):
        if weights[-i] == 0:
            break
        
        if not inventory[-i]["quantity"]:
            inventory[-i]["quantity"] = 0
        
        wav += weights[-i] * inventory[-i]["quantity"]
    
    wav /= sum(weights)

    return wav

def get_distance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c