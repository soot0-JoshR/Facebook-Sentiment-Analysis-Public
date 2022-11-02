import json
import facebook


token = "EAAIshi8WrOkBAEYL4pv6KkW3rtE2hUZBGSS6ZAD6xbLGQlRfAMLAPufNmNZAeAHwLoqtBUEiLStiyPbX4Q9YDtnUwxkEf7L7Shff9XD2iBz6T30TKhFVh8InKUgJWc5RNj8Ux6o0dROOZAodDQifY6aosfkph50lDXgF8YwkuNw13HYVL9S1"
graph = facebook.GraphAPI(token)
profile = graph.get_object(id = '354213184965483' , fields = 'about')
  
text = json.dumps(profile, indent = 4)

test = open("test.txt", "w")
test.write(text)
test.close()
