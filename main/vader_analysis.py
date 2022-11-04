
import facebook

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
len(subj_docs), len(obj_docs)

subj_docs[0]

train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]
training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs

sentiment_analyzer = SentimentAnalyzer()
all_words_neg = sentiment_analyzer.all_words([mark_negation(doc) for doc in training_docs])

unigram_feats = sentiment_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
len(unigram_feats)

sentiment_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

training_set = sentiment_analyzer.apply_features(training_docs)
test_set = sentiment_analyzer.apply_features(testing_docs)

trainer = NaiveBayesClassifier.train
classifier = sentiment_analyzer.train(trainer, training_set)

for key,value in sorted(sentiment_analyzer.evaluate(test_set).items()):
    print('{0}: {1}'.format(key, value))




# Josh's testing page
token = "ACCESS_TOKEN"
graph = facebook.GraphAPI(token)
page = graph.get_object(id='ID', fields='about,name,feed')

keywords = ["Battery electric", "BEV", "Li-ion", "Lithium-ion", "lithium batteries", "lithium battery"
            "Hydrogen Fuel Cell", "FCEV", "Fuel cell", "H2-FC",
            "Hydrogen combustion engine", "H2 ICE", "Hydrogen ICE",
            "Natural Gas", "CNG", "Compressed natural gas", "compressed natural gas"]

posts = []
kwHits = []

for each in page['feed']['data']:
    for kw in keywords:
        try:
            if each['message'] not in posts:
                if kw in each['message']:
                    kwHits.append(kw)
                    posts.append(each['message'])
        except:
            continue

print("\n\n")

post_sentences = []
i = 0

for post in posts:
    print(i+1, kwHits[i], "in message:\n", post, "\n")
    i += 1

    sentence_tokens = tokenize.sent_tokenize(post)
    sia = SentimentIntensityAnalyzer()
    for token in sentence_tokens:
        print(token)
        ss = sia.polarity_scores(token)
        for k in sorted(ss):
           print('{0}: {1}, '.format(k, ss[k]), end='')
        print("\n")
    print("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n")

