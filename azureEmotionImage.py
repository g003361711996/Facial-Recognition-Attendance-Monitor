import os
import cognitive_face as CF
import cv2



KEY = 'MY KEY'
BASE_URL = 'https://projectface.cognitiveservices.azure.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(KEY)

img_url = "KnownFaces/" + input("ENETR FILE:  ")
if not os.path.isfile(img_url):
    raise FileNotFoundError

detected_faces = CF.face.detect(img_url,attributes='age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise')

print(detected_faces)
image_result = cv2.imread(img_url)
print("Number of faces:", len(detected_faces))
cv2.rectangle(image_result, (0, 0), (36, 36), color=(215, 245, 225), thickness=3)
for face in detected_faces:
    face_box = face['faceRectangle']

    font = cv2.FONT_HERSHEY_SIMPLEX
    TextField= (face_box['left'], (face_box['top']-75))
    TextField1 = (face_box['left'], (face_box['top']-50))
    TextField2 = (face_box['left'], (face_box['top']-25))
    fontSize = 0.4
    fontColor = (0, 0, 200)
    fontThick = 1
    print(face)
    cv2.putText(image_result, str("GENDER: "+ face['faceAttributes']['gender']) 
                ,
                TextField,
                font,
                fontSize,
                fontColor,
                fontThick)
    
    cv2.putText(image_result,str("AGE: ")+str(face['faceAttributes']['age'])
                ,
                TextField1,
                font,
                fontSize,
                fontColor,
                fontThick)
    
    cv2.putText(image_result,str("ANGER%:")+str(face['faceAttributes']['emotion']['anger'])+str(", ")
                +str("CONTEMPT%:")+str(face['faceAttributes']['emotion']['contempt'])+str(", ")
                +str("DISGUST%:")+str(face['faceAttributes']['emotion']['disgust'])+str(", ")
                +str("FEAR%:")+str(face['faceAttributes']['emotion']['fear'])+str(",")
                +str("HAPPINESS%:")+str(face['faceAttributes']['emotion']['happiness'])+str(", ")
                +str("NEUTRAL%:")+str(face['faceAttributes']['emotion']['neutral'])+str(", ")
                +str("SADNESS%:")+str(face['faceAttributes']['emotion']['sadness'])+str(", ")
                +str("SURPRISE%:")+str(face['faceAttributes']['emotion']['surprise'])
                ,
                TextField2,
                font,
                fontSize,
                fontColor,
                fontThick)

    cv2.rectangle(image_result,
                  (face_box['left'], face_box['top']),
                  (face_box['left'] + face_box['width'], face_box['top'] + face_box['height']),
                  color=(215, 245, 225), thickness=3)
cv2.imshow("Detected Faces", cv2.resize(image_result, (1000, 900)))
cv2.waitKey()