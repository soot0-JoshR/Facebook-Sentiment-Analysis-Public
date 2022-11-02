
import facebook

from nltk import tokenize
from transformers import pipeline

#
"""
other models for the pipeline:
    'Seethal/sentiment_analysis_generic_dataset'
    'roberta-base'
    'facebook/bart-large-cnn'
"""

# the transformer pipeline
sentiment = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

# testing page token
token = "EAAgaO2ZCW5pgBAPf77mr8ZC4MjK5U9lxONJWhN6iqWMJY" \
        "3rE1iyVb3BbpMpNNqe2jrgaDoZCGumdRD3uReqQZAdaoX5" \
        "6geI4DXfeLbZA17XIGSEzIKiZCAAUb2GAOcqyred0ZCC5m" \
        "e7e0fQegcwcQwDvFhWHyFswjDa2NcGGKva16CAoEnRiaps"

# Facebook Graph API access
graph = facebook.GraphAPI(token)

# dictionaries to store post and comment data
post_data = graph.get_object(id='106022105635449', fields='feed')
comment_data = graph.get_object(id='106022105635449', fields='feed{comments}')

# a list of keywords to search posts for
keywords = ["Battery electric", "BEV", "Li-ion", "Lithium-ion", "lithium batteries", "lithium battery"
            "Hydrogen Fuel Cell", "FCEV", "Fuel cell", "H2-FC",
            "Hydrogen combustion engine", "H2 ICE", "Hydrogen ICE",
            "Natural Gas", "CNG", "Compressed natural gas", "compressed natural gas"]

posts = []
kwHits = []


# for getting all comments in one contiguous array
"""comments = []
i = 0
for i in range(i, len(comment_data['feed']['data'])):
    if 'comments' in comment_data['feed']['data'][i]:
        for each in comment_data['feed']['data'][i]['comments']['data']:
            comments.append(each['message'])
    i += 1"""


# append all posts that contain a keyword to the posts array
for post in post_data['feed']['data']:
    for kw in keywords:
        try:
            if post['message'] not in posts:
                if kw in post['message']:
                    kwHits.append(kw)
                    posts.append(post['message'])
        except:
            continue

print("\n\n")

# an array for storing sentences from the posts
post_sentences = []
i = 0

# loop through all posts and search for keywords.
for post in posts:
    print(i+1, kwHits[i], "in message:\n", post)

    result = sentiment(post)
    print(result, "\n")

    sentence_tokens = tokenize.sent_tokenize(post)

    for token in sentence_tokens:
        print(token)
        result = sentiment(token)
        for k in sorted(result):
            print(result)  # '{0}: {1}, '.format(k, result), end='')
        print("\n")

    j = 0

    if 'comments' in comment_data['feed']['data'][i]:
        for each in comment_data['feed']['data'][i]['comments']['data']:
            result = sentiment(each['message'])
            print("comment", j, ": ", each['message'], "\n", result)
            j += 1

    i += 1

    print("\n")

    print("////////////////////////////////////////////////////////"
          "////////////////////////////////////////////////////////"
          "////////////////////////////////////////////////////////"
          "////////////////////////////////////////////////////////\n")

