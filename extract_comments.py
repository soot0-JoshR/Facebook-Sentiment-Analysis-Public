import json
import facebook

# Josh's testing page
token = "EAAIshi8WrOkBAIR3iUkXFmQ2IQhvaoHeZBPSV9joIptO7HYv9cK0jlmtTvBi9v258JpFp0b6XQtZAmxtq72DEsX890ZAMoZC3DZC3REOZAtRuMQVZCqOnCMdArBn2M1fforQq14p13FuyplNQk1OonLiUIbQZB4xkPnMnPgOtb1EI9LZCXZChvF8eb7sNZArYb9FELAxutHPeNVvQfPZBI64IbNr"
graph = facebook.GraphAPI(token)
page = graph.get_object(id='354213184965483', fields='about,feed')
comments = graph.get_object(id='354213184965483', fields='feed{comments}')

# For loop doesnt print out right text but json file does
for each in comments['feed']['data']:
 try: 
    print(each['feed{comments}'] + '\n')
 except:
     print("No Message" + '\n')

text = json.dumps(comments, indent=4)

test = open("test.txt", "w")
test.write(text)
test.close()
