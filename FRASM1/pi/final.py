import time

import cv2
import requests

from CONSTANTS import FACE_API_KEY, FACE_BASE_URL, CAPTURE_INTERVAL, \
    REST_SERVER_URL, FACE_GROUP_ID, CAMERA_NAME
from camera.Camera import Camera
from face.FaceAPIWrapper import FaceAPIWrapper
from utils import  upload_to_s3, current_time_to_string, create_dir_if_not_exists, save_dict_to_file, load_dict_from_file


def main():
    person_group_id = FACE_GROUP_ID
    display_image = False
    
    face_api_wrapper = FaceAPIWrapper(FACE_API_KEY, FACE_BASE_URL)
    create_dir_if_not_exists('captured_images/' + CAMERA_NAME)
   
    print("Capturing Image every ", CAPTURE_INTERVAL, " seconds...")

    i = 0

    while 1:
        try:
            image_filename = 'captured_images/' + CAMERA_NAME + "/" + current_time_to_string() + ".jpg"
            image = Camera().capture_image()
            cv2.imwrite(image_filename, image)

            if display_image:
                cv2.imshow("Camera Image", image)
                cv2.waitKey(1)

            image_link = upload_to_s3(image_filename)
            image_url = 'https://mybuckfucket.s3-eu-west-1.amazonaws.com/public_folder/'+image_filename
            face_ids = face_api_wrapper.detect_faces(image=image_filename)
            i += 1
            print(i, "Captured at ", current_time_to_string())
            print("S3 url",image_url)
            if face_ids:
                person_ids = \
                    face_api_wrapper.identify_faces(face_ids=face_ids,
                                                    large_person_group=person_group_id)
                req_ids = [{id} for id in person_ids]
                print("Detected Faces...", req_ids)
                contents=load_dict_from_file('json.txt')
                
                #my_data=(contents[0]['faceAttributes'])
                requests.post('http://127.0.0.1:8000/students/', data={
                    'attributes' : contents,
                    'name' : "Darragh",
                    'time_date' : current_time_to_string(),
                    'face_ids' : person_ids,
                    'image_link' : image_url,
                })
                print("#####",data)
                #print(contents[0]['faceAttributes']['emotion'])
                #requests.post('http://127.0.0.1:8000/students/', data=contents)
                

            time.sleep(CAPTURE_INTERVAL)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # initial_setup()
    main()
