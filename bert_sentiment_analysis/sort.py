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


def has_other_keyword(text):
    text_list = text.split(" ")
    for word in text_list:
        for kw in keywords["electric"]:
            if kw in word:
                return "electric"
        for kw in keywords["hydrogen"]:
            if kw in word:
                return "hydrogen"
        for kw in keywords["natural_gas"]:
            if kw in word:
                return "natural_gas"
    return False


data = []

with open("object_list.json", "r", encoding="utf-8") as dataFile:
    data = json.loads(dataFile.read())

dataFile.close()

for e in data:
    if e["keyword"] in keywords["general"]:
        otherKeyword = has_other_keyword(e["text"])
        if otherKeyword:
            e.update({"keyword": otherKeyword})
        else:
            e.update({"keyword": "general"})
    elif e["keyword"] in keywords["electric"]:
        e.update({"keyword": "electric"})
    elif e["keyword"] in keywords["hydrogen"]:
        e.update({"keyword": "hydrogen"})
    elif e["keyword"] in keywords["natural_gas"]:
        e.update({"keyword": "natural_gas"})

with open("object_list.json", "w", encoding="utf-8") as newFile:
    json.dump(data, newFile, ensure_ascii=False).encode("utf-8")
newFile.close()

