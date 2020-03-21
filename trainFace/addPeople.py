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

# adds faces to the created people in PersonGroup
def addFaceToPerson(list):
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key':KEY}
    conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
    for item in list:
        params = urllib.parse.urlencode({'personGroupId': group_id, 'personId': item[1]}) # item[1] is the personId created from addPeople()
        directory = '/home/pi/Desktop/ProjectSamples/People/'+item[0] # item[0] is peron's name, each person should have a directory named after them filled with photos of them
        for filename in os.listdir(directory):
            if filename.endswith('.jpeg'): # adjust this depending on the file type of your photos
                filePath = os.path.join(directory, filename) # creates full file path
                body = open(filePath,'rb')
                conn.request("POST", "/face/v1.0/persongroups/{employees}/persons/"+item[1]+"/persistedFaces?%s" % params, body, headers)
                response = conn.getresponse()
                data = json.loads(response.read()) # successful run will print persistedFaceId
                print(data)
    conn.close()

addFaceToPerson(addPeople())
