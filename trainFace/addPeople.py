import urllib, http.client, base64, json
import sys
import os

people = ['Barack','Jeff','Mia','Darragh', 'Alice']
nameAndID = [] # empty list for persons' name and personId
group_id = 'employees'
KEY = 'fc36b866a9c84de3bdc3c29df2b7705c'

# creates people in personGroup of specified group_Id
def addPeople():
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}
    params = urllib.parse.urlencode({'personGroupId': group_id})
    conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
    for name in people:
        body = "{'name':'"+name+"'}"
        conn.request("POST", "/face/v1.0/persongroups/{employees}/persons?%s" % params, body, headers)
        response = conn.getresponse()
        data = json.loads(response.read()) # turns response into index-able dictionary
        out = name+"'s ID: " +data['personId']
        print(out)
        nameAndID.append((name, data['personId'])) # fills list with tuples of name and personId
    conn.close()
    return nameAndID

