import json
import facebook

# Josh's testing page
token = "EAAgaO2ZCW5pgBANLEurGzBId3lgrURnZBkKl3p8NH6EmemhknxcnQsvaRZCVkrVyZARLkBAfve9qWl5Wjtv69d7bDoPvZCVcjeSTMKNcVQROwlft3p4lscLVQ2JrSBhOZBn84PmuBDf26wFnQDmDxPKIcwvdCUmGgwegtpRFMT7MTCr0rKyshb"
graph = facebook.GraphAPI(token)
page = graph.get_object(id='106022105635449', fields='about,name,feed')

for each in page['feed']['data']:
    try:
        print(each['message'] + '\n')
    except:
        print("No message")

text = json.dumps(page, indent=4)

test = open("test.txt", "w")
test.write(text)
test.close()
