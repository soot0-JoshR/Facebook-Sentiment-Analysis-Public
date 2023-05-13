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

overallResultData = {"count": count,
                     "electric_count": eCount, "electricScores": electricScores,
                     "hydrogen_count": hCount, "hydrogenScores": hydrogenScores,
                     "naturalG_count": nCount, "naturalGScores": naturalGScores,
                     "generalP_count": gCount, "generalPScores": generalPScores,
                     "individualResultData": {}}

# update the sentiment scores in each power-train type
for sentiment in sentiments:
    overallResultData["electricScores"].update(
        {sentiment: overallResultData["electricScores"][sentiment] / overallResultData["electric_count"]})
    overallResultData["hydrogenScores"].update(
        {sentiment: overallResultData["hydrogenScores"][sentiment] / overallResultData["hydrogen_count"]})
    overallResultData["naturalGScores"].update(
        {sentiment: overallResultData["naturalGScores"][sentiment] / overallResultData["naturalG_count"]})
    overallResultData["generalPScores"].update(
        {sentiment: overallResultData["generalPScores"][sentiment] / overallResultData["generalP_count"]})


print(count)

individualResultData = {}
for e in data:
    individual = {"posts": [],
                  "post_count": 0,
                  "e_count": 0,
                  "electric": {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                               "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0},
                  "h_count": 0,
                  "hydrogen": {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                               "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0},
                  "n_count": 0,
                  "natural_gas": {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                                  "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0},
                  "g_count": 0,
                  "general": {"positive": 0.0, "neutral": 0.0, "negative": 0.0,
                              "joy": 0.0, "optimism": 0.0, "anger": 0.0, "sadness": 0.0}
                  }

    if e["author_id"] not in individualResultData:
        if e["keyword"] == "electric":
            individual["e_count"] = 1  # set the number of electric posts by this author to 1
        if e["keyword"] == "hydrogen":
            individual["h_count"] = 1  # set the number of hydrogen fuel cell posts by this author to 1
        if e["keyword"] == "natural_gas":
            individual["n_count"] = 1  # set the number natural gas combustion of posts by this author to 1
        if e["keyword"] == "general":
            individual["g_count"] = 1  # set the number of alternative power-train posts by this author to 1
        for sentiment in sentiments:
            individual[e["keyword"]][sentiment] = float(e[sentiment])
        individual["posts"].append(e["conversation_id"])
        individualResultData[e["author_id"]] = individual  # set the keys equal to e if they do not already exist
    else:
        individual = individualResultData[e["author_id"]]
        if e["keyword"] == "electric":
            individual["e_count"] += 1  # increment the number of electric posts by this author by 1
        if e["keyword"] == "hydrogen":
            individual["h_count"] += 1  # increment the number of hydrogen fuel cell posts by this author by 1
        if e["keyword"] == "natural_gas":
            individual["n_count"] += 1  # increment the number natural gas combustion of posts by this author by 1
        if e["keyword"] == "general":
            individual["g_count"] += 1  # increment the number of alternative power-train posts by this author by 1
        for sentiment in sentiments:
            individual[e["keyword"]][sentiment] += float(e[sentiment])
        individual["posts"].append(e["conversation_id"])
        individualResultData[e["author_id"]] = individual

for e in individualResultData:
    individualResultData[e]["post_count"] = len(individualResultData[e]["posts"])
    if individualResultData[e]["e_count"] > 0:
        for sentiment in sentiments:
            individualResultData[e]["electric"].update(
                {sentiment: individualResultData[e]["electric"][sentiment] / individualResultData[e]["e_count"]})
    if individualResultData[e]["h_count"] > 0:
        for sentiment in sentiments:
            individualResultData[e]["hydrogen"].update(
                {sentiment: individualResultData[e]["hydrogen"][sentiment] / individualResultData[e]["h_count"]})
    if individualResultData[e]["n_count"] > 0:
        for sentiment in sentiments:
            individualResultData[e]["natural_gas"].update(
                {sentiment: individualResultData[e]["natural_gas"][sentiment] / individualResultData[e]["n_count"]})
    if individualResultData[e]["g_count"] > 0:
        for sentiment in sentiments:
            individualResultData[e]["general"].update(
                {sentiment: individualResultData[e]["general"][sentiment] / individualResultData[e]["g_count"]})

overallResultData["individualResultData"] = individualResultData

with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(overallResultData, file, ensure_ascii=False)
file.close()
