import urllib, http.client, base64

group_id = 'employees'
KEY = 'MY KEY'

headers = {'Ocp-Apim-Subscription-Key': KEY}
params = urllib.parse.urlencode({'personGroupId': group_id})
conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
conn.request("GET", "/face/v1.0/persongroups/"+group_id+"/training?%s" % params, "{body}", headers)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()