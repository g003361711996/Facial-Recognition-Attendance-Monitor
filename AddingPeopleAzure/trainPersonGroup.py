import urllib, http.client, base64

group_id = 'students'
KEY = 'mykey#########'

params = urllib.parse.urlencode({'personGroupId': group_id})
headers = {'Ocp-Apim-Subscription-Key': KEY}

conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
conn.request("POST", "/face/v1.0/persongroups/students/train?%s" % params, "{body}", headers)
response = conn.getresponse()
data = response.read()
print(data) 