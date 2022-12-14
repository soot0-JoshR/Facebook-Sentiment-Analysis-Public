import json
import facebook

# Testing page

# Find out how to automate making a token, then assigns GraphAPI to graph
token = "ACCESS_TOKEN"
graph = facebook.GraphAPI(token)

# Input page ID and return the adjacent fields "about" and "feed" then get feed comments and writes to comments
page = graph.get_object(id='USER_ID', fields='about,feed')
comments = graph.get_object(id='USER_ID', fields='feed{comments}')

# json dumps are put into post_text
post_text = json.dumps(page, indent=4)

# post_text is then written into file post
post = open("posts.txt", "a")
post.write(post_text)
post.close()

# Loop to print out comments with post id for testing
for i in comments['feed']['data']:
  ID = i['id']
  # separate the post ID from the comment ID and display post with correlating comments    
  post_Id = ID.partition("_")[2]
  # Prints post Id and realted comments
  try:
    comment_data = i['comments']
    print ("Post ID = " + post_Id)
    for j in comment_data['data']:
      print (j['message'] + "\n")
    print("\n\n")
  except:
    pass

#repeat step above but for post comments
comment_text = json.dumps(comments, indent=4)

comment = open("comment.txt", "a")
comment.write(comment_text)
comment.close()
