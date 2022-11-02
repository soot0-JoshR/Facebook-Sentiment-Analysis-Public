import json
import facebook

token = "ACCESS_TOKEN"
graph = facebook.GraphAPI(token)
page = graph.get_object(id='PAGE_ID', fields='about,name,feed')

for each in page['feed']['data']:
    try:
        print(each['message'] + '\n')
    except:
        print("No message")

text = json.dumps(page, indent=4)

test = open("test.txt", "w")
test.write(text)
test.close()
