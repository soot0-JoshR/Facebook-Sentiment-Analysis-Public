import os
import numpy
import json
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax

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


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)

model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# transformer pipeline
# sentiment = pipeline('sentiment-analysis', model=MODEL)

# a list of keywords to search posts for
keywords = ["Battery electric", "electric", "electro", "BEV", "Li-ion", "Lithium-ion", "lithium batteries",
            "lithium battery",
            "Hydrogen Fuel Cell", "FCEV", "Fuel cell", "H2-FC",
            "Hydrogen combustion engine", "H2 ICE", "Hydrogen ICE",
            "Natural Gas", "CNG", "Compressed natural gas", "compressed natural gas"]

posts = []
kwHits = []

# for scraping_output json file
jsonFile = open("scraping_output.json", encoding='utf-8')
pages = json.load(jsonFile)

post = ""

for page in pages:
    for kw in keywords:
        if kw in page["postText"]:  # if we find a keyword
            print(kw, " in post by ", page["author"], ": ")  # print header message
            print(page["postText"], "\n")  # print the post text
            post = preprocess(page["postText"])  # generalize text like links and usernames
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
                print(f" {label} {numpy.round(float(results), 4)}")  # print the result

            print("----------------------\n")

            for comment in page["comments"]:
                for kW in keywords:
                    if kW in comment:  # if we find a keyword
                        print(kW, " in comment by ", comment["author"], ": ")  # print header message
                        print(comment["text"], "\n")  # print the comment text
                        post = preprocess(comment["text"])  # generalize text such as links and usernames
                        post = clean(post)  # remove generalized text

                        encoded_input = tokenizer(post, return_tensors='pt')  # prepare post text for the model
                        result = model(**encoded_input)  # feed our encoded post text into the model
                        scores = result[0][0].detach().numpy()  # create a numpy array from the model output
                        scores = softmax(
                            scores)  # transform scores array values into probabilities (values between 0 and 1)

                        ranked = numpy.argsort(scores)  # store the sorted indices of scores in ranked
                        ranked = ranked[::-1]  # reverse the array of indices
                        for e in range(scores.shape[0]):  # for each value in the numpy array
                            label = config.id2label[ranked[e]]  # get the labels for our result
                            results = scores[ranked[e]]  # get the results (the probability values)
                            print(f" {label} {numpy.round(float(results), 4)}")  # print the result
                        print("----------------------\n")


path = "C:/Users/r1tt3/PycharmProjects/pythonProject/text/"
dir_list = os.listdir(path)
# print(dir_list)
os.chdir(path)
for filename in dir_list:
    with open(filename, "r") as file:
        file_text = file.read()
        for kw in keywords:
            if kw in file_text:
                file_text = preprocess(file_text)
                file_text = clean(file_text)
                print(kw, " in ", filename, ": ")  # print header message
                print(file_text, "\n")  # print the post text
                encoded_input = tokenizer(file_text, return_tensors='pt')  # prepare post text for the model
                result = model(**encoded_input)  # feed our encoded post text into the model
                scores = result[0][0].detach().numpy()  # create a numpy array from the model output
                scores = softmax(scores)  # transform scores array values into probabilities (values between 0 and 1)

                ranked = numpy.argsort(scores)  # store the sorted indices of scores in ranked
                ranked = ranked[::-1]  # reverse the array of indices
                for e in range(scores.shape[0]):  # for each value in the numpy array
                    label = config.id2label[ranked[e]]  # get the labels for our result
                    results = scores[ranked[e]]  # get the results (the probability values)
                    print(f" {label} {numpy.round(float(results), 4)}")  # print the result
                print("----------------------\n")
