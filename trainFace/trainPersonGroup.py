import urllib, http.client, base64

group_id = 'employees'
KEY = 'MY_KEY'

params = urllib.parse.urlencode({'personGroupId': group_id})
headers = {'Ocp-Apim-Subscription-Key': KEY}

conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
conn.request("POST", "/face/v1.0/persongroups/employees/train?%s" % params, "{body}", headers)
response = conn.getresponse()
data = response.read()
print(data) # if successful prints empty json body