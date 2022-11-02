import json
import facebook


token = "ACCESS_TOKEN"
graph = facebook.GraphAPI(token)
profile = graph.get_object(id = 'USER_ID' , fields = 'about')
  
text = json.dumps(profile, indent = 4)

test = open("test.txt", "w")
test.write(text)
test.close()
