import requests
import urllib, http.client, base64

KEY = '###mykey###'

group_id = 'students'
body = '{"name": "Students"}'
params = urllib.parse.urlencode({'personGroupId': group_id})
headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}


conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
conn.request("PUT", "/face/v1.0/persongroups/{personGroupId}?%s" % params, body, headers)
response = conn.getresponse()
data = response.read()

print(data)
conn.close()