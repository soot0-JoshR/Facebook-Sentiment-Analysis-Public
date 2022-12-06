import json

with open("object_list.json", "r", encoding="utf-8") as dataFile:
    data = json.loads(dataFile.read())

dataFile.close()

sentiments = ["positive", "neutral", "negative", "joy", "optimism", "anger", "sadness"]

electricScores = {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                  "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0}

hydrogenScores = {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                  "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0}

naturalGScores = {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                  "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0}

generalPScores = {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                  "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0}

eCount = 0
hCount = 0
nCount = 0
gCount = 0
count = 0

for e in data:
    if e["keyword"] == "electric":
        eCount += 1
        for sentiment in sentiments:
            electricScores[sentiment] += float(e[sentiment])
    if e["keyword"] == "hydrogen":
        hCount += 1
        for sentiment in sentiments:
            hydrogenScores[sentiment] += float(e[sentiment])
    if e["keyword"] == "natural_gas":
        nCount += 1
        for sentiment in sentiments:
            naturalGScores[sentiment] += float(e[sentiment])
    if e["keyword"] == "general":
        gCount += 1
        for sentiment in sentiments:
            generalPScores[sentiment] += float(e[sentiment])
    count += 1

resultData = {"count": count,
              "electric_count": eCount, "electricScores": electricScores,
              "hydrogen_count": hCount, "hydrogenScores": hydrogenScores,
              "naturalG_count": nCount, "naturalGScores": naturalGScores,
              "generalP_count": gCount, "generalPScores": generalPScores}

# update the sentiment scores in each powertrain type
for e in sentiments:
    resultData["electricScores"].update({e: resultData["electricScores"][e] / resultData["electric_count"]})
    resultData["hydrogenScores"].update({e: resultData["hydrogenScores"][e] / resultData["hydrogen_count"]})
    resultData["naturalGScores"].update({e: resultData["naturalGScores"][e] / resultData["naturalG_count"]})
    resultData["generalPScores"].update({e: resultData["generalPScores"][e] / resultData["generalP_count"]})


print(count)

with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(resultData, file, ensure_ascii=False).encode("utf-8")

dataFile.close()
