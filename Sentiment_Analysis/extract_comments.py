import json
import facebook


token = "ACCESS_TOKEN"
graph = facebook.GraphAPI(token)
page = graph.get_object(id='PAGE_ID', fields='about,feed')
comments = graph.get_object(id='PAGE_ID', fields='feed{comments}')

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
