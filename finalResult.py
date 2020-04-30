#*****securityFaceId.py*****#

import requests
from operator import itemgetter
from picamera import PiCamera
import sys
import json
import os
import urllib, http.client, base64, json
import boto3
import datetime
import time

import RPi.GPIO as GPIO
import time 
BaseDirectory = '/home/pi/Desktop/ProjectSamples/Photos/' # directory where picamera photos are stored
KEY = 'MY_KEY' # authorization key for azure
group_id = 'employees' # name of personGroup
bucketName = 'MY_NAME' # aws s3 bucket name

#*****Camera Setup*****#
camera = PiCamera() # initiate camera
#camera.rotation = 180 # Used to correct orientation of camera

def iter():
    for fileName in os.listdir(directory):
        if fileName.endswith('.jpg'):
            filePath = os.path.join(directory, fileName) # joins directory path with filename to create file's full path
            fileList.append(filePath)
            detect(filePath)

# detects faces in images from previously stated directory using azure post request
def detect(img_url):
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}
    body = open(img_url,'rb')

    params = urllib.parse.urlencode({'returnFaceId': 'true'})
    conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
    conn.request("POST", '/face/v1.0/detect?%s' % params, body, headers)
    response = conn.getresponse()
    photo_data = json.loads(response.read())

    if not photo_data: # if post is empty (meaning no face found)
        print('No face identified')
    else: # if face is found
        for face in photo_data: # for the faces identified in each photo
            faceIdList.append(str(face['faceId'])) # get faceId for use in identify

# Takes in list of faceIds and uses azure post request to match face to known faces
def identify(ids):
    if not faceIdList: # if list is empty, no faces found in photos
        result = [('n', .0), 'n'] # create result with 0 confidence
        return result # return result for use in main
    else: # else there is potential for a match
        headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}
        params = urllib.parse.urlencode({'personGroupId': group_id})
        body = "{'personGroupId':'employees', 'faceIds':"+str(ids)+", 'confidenceThreshold': '.5'}"
        conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
        conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
        response = conn.getresponse()

        data = json.loads(response.read()) # turns response into index-able dictionary

        for resp in data:
            candidates = resp['candidates']
            for candidate in candidates: # for each candidate in the response
                confidence = candidate['confidence'] # retrieve confidence
                personId = str(candidate['personId']) # and personId
                confidenceList.append((personId, confidence))
        conn.close()
        SortedconfidenceList = zip(confidenceList, fileList) # merge fileList and confidence list
        sortedConfidence = sorted(SortedconfidenceList, key=itemgetter(1)) # sort confidence list by confidence
        return sortedConfidence[-1] # returns tuple with highest confidence value (sorted from smallest to biggest)


# takes in person_id and retrieves known person's name with azure GET request
def getName(person_Id):
    headers = {'Ocp-Apim-Subscription-Key': KEY}
    params = urllib.parse.urlencode({'personGroupId': group_id, 'personId': person_Id})

    conn = http.client.HTTPSConnection('projectface.cognitiveservices.azure.com')
    conn.request("GET", "/face/v1.0/persongroups/{"+group_id+"}/persons/"+person_Id+"?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    name = data['name']
    conn.close()
    return name


# uses aws s3 to upload photos
def uploadPhoto(fName):
    s3=boto3.resource('s3')
    data = open(fName, 'rb')
    s3.Bucket(bucketName).put_object(Key=fName, Body=data, ContentType = 'image/jpeg')

    # makes uploaded image link public
    object_acl = s3.ObjectAcl(bucketName, fName)
    response = object_acl.put(ACL='public-read')

    link = 'https://s3.amazonaws.com/'+bucketName+'/'+fName
    return link

#*****Main*****#
count = 0
while True:
    # lists are refreshed for every incident of motion
    fileList = [] # list of filePaths that were passed through as images
    faceIdList = [] # list for face id's generated using api - detect
    confidenceList = [] # list of confidence values derived from api - identify
   
    
    count += 1 # count allows for a new directory to be made for each set of photos
    directory = BaseDirectory+str(count)+'/'
    print("Detected")
    os.mkdir(directory) # make new directory for photos to be uploaded to
    print(count)
    print(directory)
    for x in range(0,3):
        date = datetime.datetime.now().strftime('%m_%d_%Y_%M_%S_') # change file name for every photo
        camera.capture(directory + date +'.jpg')
        time.sleep(1) # take photo every second
    iter()
    result = identify(faceIdList)
    if result[0][1] > .7: # if confidence is greater than .7 get name of person
        print(result[0][0])
        if result[0][0] == 'ce730530-f753-42ab-b907-7f60b2e12902':
            print ('Darragh')
        for files in fileList:
            link = uploadPhoto(files) # upload all photos of incident for evidence
    else:
        print("Unknown")
        #twilio('Motion Detected in the Office. Incident:'+count, link) # send message
