import json

keywords = {

    "electric": [
        "battery", "Battery", "Electric",
        "electric", "Electro", "electro",
        "BEV", "li-ion", "Li-ion",
        "Lithium-ion", "lithium-ion", "lithium",
        "batteries", "Batteries", "Lithium"]
    ,

    "hydrogen": [
        "Hydrogen", "fuelcell", "Fuel Cell", "hydrogen",
        "fuel cell", "FCEV", "Fuel cell",
        "H2-FC", "h2-FC", "H2 ICE", "h2 ICE",
        "Hydrogen ICE", "power cell", "hydrogen ICE"]
    ,

    "natural_gas": [
        "Natural Gas", "natural gas", "CNG", "naturalgas",
        "Compressed natural gas", "compressed natural gas"]
    ,

    "general": [
        "Alternative fuel", "alternative fuel",
        "alt-fuel", "powertrain", "Powertrain",
        "drivetrain", "Drivetrain", "general"]
    }


def has_other_keyword(key, text):
    text_list = text.split(" ")

    key_list = []

    if key == "general":
        for word in text_list:
            for kw in keywords["electric"]:
                if kw in word:
                    key_list.append("electric")
            for kw in keywords["hydrogen"]:
                if kw in word:
                    key_list.append("hydrogen")
            for kw in keywords["natural_gas"]:
                if kw in word:
                    key_list.append("natural_gas")
    elif key == "electric":
        for word in text_list:
            for kw in keywords["hydrogen"]:
                if kw in word:
                    key_list.append("hydrogen")
            for kw in keywords["natural_gas"]:
                if kw in word:
                    key_list.append("natural_gas")
    elif key == "hydrogen":
        for word in text_list:
            for kw in keywords["electric"]:
                if kw in word:
                    key_list.append("electric")
            for kw in keywords["natural_gas"]:
                if kw in word:
                    key_list.append("natural_gas")
    elif key == "natural_gas":
        for word in text_list:
            for kw in keywords["electric"]:
                if kw in word:
                    key_list.append("electric")
            for kw in keywords["hydrogen"]:
                if kw in word:
                    key_list.append("hydrogen")

    if len(key_list) > 0:
        return key_list

    return False


data = []

with open("object_list.json", "r", encoding="utf-8") as dataFile:
    data = json.loads(dataFile.read())

dataFile.close()

for i in range(0, len(data), 1):
    if data[i]["keyword"] in keywords["general"]:
        otherKeywords = has_other_keyword("general", data[i]["text"])
        if otherKeywords:
            for e in otherKeywords:
                data.append(data[i])
                data[-1].update({"keyword": e})
        else:
            data[i].update({"keyword": "general"})
    elif data[i]["keyword"] in keywords["electric"]:
        otherKeywords = has_other_keyword("electric", data[i]["text"])
        if otherKeywords:
            for e in otherKeywords:
                data.append(data[i])
                data[-1].update({"keyword": e})
        else:
            data[i].update({"keyword": "electric"})
    elif data[i]["keyword"] in keywords["hydrogen"]:
        otherKeywords = has_other_keyword("hydrogen", data[i]["text"])
        if otherKeywords:
            for e in otherKeywords:
                data.append(data[i])
                data[-1].update({"keyword": e})
        else:
            data[i].update({"keyword": "hydrogen"})
    elif data[i]["keyword"] in keywords["natural_gas"]:
        otherKeywords = has_other_keyword("natural_gas", data[i]["text"])
        if otherKeywords:
            for e in otherKeywords:
                data.append(data[i])
                data[-1].update({"keyword": e})
        else:
            data[i].update({"keyword": "natural_gas"})

with open("object_list.json", "w", encoding="utf-8") as newFile:
    json.dump(data, newFile, ensure_ascii=False).encode("utf-8")
newFile.close()

