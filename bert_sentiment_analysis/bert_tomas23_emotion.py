import os
import numpy
import json
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
import csv
import time

#
"""
# unused code
def clean(text):
    rwords = ['@user', 'http', '#']
    for word in rwords:
        text = text.replace(word, "")
    return text


def preprocess(text):
    text = text.replace('\n', ' ')
    new_text = []
    for t in text.split(" "):
        t = '#' if t.startswith('\\x') else t
        t = '#' if t.startswith('#') else t
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

other models for the pipeline:
    'distilbert-base-uncased-finetuned-sst-2-english'
    'Seethal/sentiment_analysis_generic_dataset'
    'roberta-base'
    'facebook/bart-large-cnn'
    'cardiffnlp/twitter-roberta-base-sentiment'
    'cardiffnlp/twitter-roberta-base-sentiment-latest'
    'Tomas23/twitter-roberta-base-mar2022-finetuned-emotion'
"""


MODEL = f"Tomas23/twitter-roberta-base-mar2022-finetuned-emotion"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)

model = AutoModelForSequenceClassification.from_pretrained(MODEL)

print("\n\n")

# transformer pipeline
# sentiment = pipeline('sentiment-analysis', model=MODEL)

# a list of keywords to search posts for
keywords = ["battery", "Battery", "Electric", "electric", "Electro", "electro", "BEV", "li-ion", "Li-ion",
            "Lithium-ion", "lithium-ion",
            "lithium", "batteries", "Batteries", "Lithium",
            "Hydrogen", "Fuel Cell", "hydrogen", "fuel cell", "FCEV", "Fuel cell", "H2-FC", "h2-FC"
            "H2 ICE", "h2 ICE", "Hydrogen ICE", "power cell",
            "hydrogen ICE", "Natural Gas", "natural gas", "CNG", "Compressed natural gas", "compressed natural gas"
            "Alternative fuel", "alternative fuel", "powertrain", "Powertrain", "drivetrain", "Drivetrain"]

posts = []
kwHits = []
#dataList = list(csv.reader(open('data.csv', 'rt', encoding='utf-8'), delimiter='\t'))
with open('data.json', 'r', encoding="utf-8") as file:
    dataList = json.loads(file.read())

file.close()

"""print(dataList)

d = dict()
key = dataList[6][0]      # cell A7
value = dataList[6][3]    # cell D7
d[key] = value       # add the entry to the dictionary
print(d[key])"""

#dataList[e][2]

for e in dataList:
    for kw in keywords:
        if kw in e[2]:
            kwHits.append(e)
            kwHits[len(kwHits)-1].append(kw)
            break


for kwHit in kwHits:
    post = kwHit[2]
    post = preprocess(post)  # generalize text such as links and usernames
    post = clean(post)  # remove generalized text

    encoded_input = tokenizer(post, return_tensors='pt')  # prepare post text for the model
    result = model(**encoded_input)  # feed our encoded post text into the model
    scores = result[0][0].detach().numpy()  # create a numpy array from the model output
    scores = softmax(scores)  # transform scores array values into probabilities (values between 0 and 1)

    ranked = numpy.argsort(scores)  # store the sorted indices of scores in ranked
    ranked = ranked[::-1]  # reverse the array of indices
    for e in range(scores.shape[0]):  # for each value in the numpy array
        label = config.id2label[ranked[e]]  # get the labels for our result
        results = scores[ranked[e]]  # get the results (the probability values)
        # print(f" {label} {numpy.round(float(results), 4)}")  # print the result
        kwHit.append(f"{numpy.round(float(results), 4)}")


with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(kwHits, file, ensure_ascii=False).encode("utf-8")

