import http.client, json  
from picamera import PiCamera  
from time import sleep  
import sys   
 
#cognitive settings  
subscription_key = 'MY KEY'  
uri_base = 'southcentralus.api.cognitive.microsoft.com'  
analyze_uri = "/vision/v1.0/analyze?%s"  
  
face_detect_uri = "/face/v1.0/detect?returnFaceId=true"  
face_verify_uri = "/face/v1.0/verify"  
base_face_id = ""  
base_face_file = '/home/pi/test.jpg'  # this file was created from the camera test  
 
#other settings  
fileName = "/home/pi/enzo/image.jpg"  # this file is created every few seconds  
headers = dict()  
headers['Ocp-Apim-Subscription-Key'] = subscription_key  
headers['Content-Type'] = "application/octet-stream"  
  
headers_appjson = dict()  
headers_appjson['Ocp-Apim-Subscription-Key'] = subscription_key  
headers_appjson['Content-Type'] = "application/json"  
  
lastValue = False   
camera = PiCamera()  
  
def capturePicture(fipathToFileInDiskle):  
    camera.capture(fipathToFileInDiskle)   
 
#METHOD THAT RETURNS A FACEID FROM AN IMAGE STORED ON DISK  
def getFaceId(pathToFileInDisk, headers):  
      
    with open( pathToFileInDisk, "rb" ) as f:  
        inputdata = f.read()  
    body = inputdata  
    faceId = ""  
  
    try:  
        conn = http.client.HTTPSConnection(uri_base)  
        conn.request("POST", face_detect_uri, body, headers)  
        response = conn.getresponse()  
        data = response.read().decode('utf-8')                   
        #print(data)  
        parsed = json.loads(data)  
          
        if (len(parsed) > 0):  
            print (parsed)  
            faceId = parsed[0]['faceId']  
            print(faceId)  
        conn.close()   
  
    except Exception as e:   
            print('Error:')  
            print(e)   
  
    return faceId   
  
def compareFaces(faceId1, faceId2):  
  
    identical = False  
      
    try:  
        body = '{ "faceId1": "' + faceId1 + '", "faceId2": "' + faceId2 + '" }'  
        print(body)  
          
        conn = http.client.HTTPSConnection(uri_base)  
        conn.request("POST", face_verify_uri, body, headers_appjson)  
        response = conn.getresponse()  
        data = response.read().decode('utf-8')  
        print(data)  
        parsed = json.loads(data)  
        identical = parsed['isIdentical']  
          
        conn.close()   
  
    except Exception as e:   
            print('Error:')  
            print(e)   
  
    return identical   
 
# Main code starts here print('starting...')   
print('starting...')  
 
# Get the face id of the base image - this faceId is valid for 24 hours  
faceId1 = getFaceId(base_face_file, headers)  
  
while True:  
    try:  
        print("calling camera...")  
        capturePicture(fileName)  
        print("calling Azure Cognitive service...")  
        faceId2 = getFaceId(fileName, headers)  
        if (len(faceId2) > 0):  
            isSame = compareFaces(faceId1, faceId2)  
            if isSame:  
                # Same face detected... send the message  
                print("SAME FACE DETECTED")   
    except:  
        print("Error:", sys.exc_info()[0])   
  
    sleep(2)   