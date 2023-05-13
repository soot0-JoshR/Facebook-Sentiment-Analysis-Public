from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmaximport numpy
import transformers
import datetime
import json
import csv

if transformers.is_tf_available():
    print("TensorFlow is being used.")
elif transformers.is_torch_available():
    print("PyTorch is being used.")
else:
    print("Neither TensorFlow nor PyTorch is available.")

# using this to keep track of how long it takes to process the data
now = datetime.datetime.now()
print("start time: " + str(now) + "\n")

#
"""
other models for the pipeline:
    'distilbert-base-uncased-finetuned-sst-2-english'
    'Seethal/sentiment_analysis_generic_dataset'
    'roberta-base'
    'facebook/bart-large-cnn'
    'cardiffnlp/twitter-roberta-base-sentiment'
    'cardiffnlp/twitter-roberta-base-sentiment-latest'
    'Tomas23/twitter-roberta-base-mar2022-finetuned-emotion'
"""

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)

model = AutoModelForSequenceClassification.from_pretrained(MODEL)

print("\n\n")

# a list of keywords to search for in posts
keywords = ["battery", "Battery", "Electric", "electric", "Electro", "electro", "BEV", "li-ion", "Li-ion",
            "Lithium-ion", "lithium-ion",
            "lithium", "batteries", "Batteries", "Lithium",
            "Hydrogen", "Fuel Cell", "hydrogen", "fuel cell", "FCEV", "Fuel cell", "H2-FC", "h2-FC"
            "H2 ICE", "h2 ICE", "Hydrogen ICE", "power cell",
            "hydrogen ICE", "Natural Gas", "natural gas", "CNG", "Compressed natural gas", "compressed natural gas"
            "Alternative fuel", "alternative fuel", "powertrain", "Powertrain", "drivetrain", "Drivetrain"]

posts = []
kwHits = []

# a list made from the data files
dataList = list(csv.reader(open('data_1.csv', 'rt', encoding='utf-8'), delimiter=','))
dataList += list(csv.reader(open('data_2.csv', 'rt', encoding='utf-8'), delimiter=','))
dataList += list(csv.reader(open('data_3.csv', 'rt', encoding='utf-8'), delimiter=','))
dataList += list(csv.reader(open('data_4.csv', 'rt', encoding='utf-8'), delimiter=','))


for e in dataList:
    for kw in keywords:
        if kw in e[2]:
            kwHits.append(e)
            kwHits[len(kwHits)-1].append(kw)
            break

for kwHit in kwHits:
    post = kwHit[2]

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
        # add the scores without labels to kwHits
        kwHit.append(f"{numpy.round(float(results), 4)}")
        # kwHit.append(f" {label} {numpy.round(float(results), 4)}")

now = datetime.datetime.now()
print("finish time: " + str(now) + "\n")

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(kwHits, file, ensure_ascii=False)
