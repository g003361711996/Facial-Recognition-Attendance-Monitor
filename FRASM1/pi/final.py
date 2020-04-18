import time

import cv2
import requests

from CONSTANTS import FACE_API_KEY, CAMERA_NAME
from camera.Camera import Camera
from face.FaceAPIWrapper import FaceAPIWrapper
from utils import  upload_to_s3, current_time_to_string, create_dir_if_not_exists,


def main():
    person_group_id = 'students'
    display_image = False
    
    face_api_wrapper = FaceAPIWrapper(FACE_API_KEY, 'https://projectface.cognitiveservices.azure.com/face/v1.0')
    create_dir_if_not_exists('captured_images/' + CAMERA_NAME)
   sec = 50
    print("Capturing Image every ", sec, " seconds...")

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
            face_ids = face_api_wrapper.detect_faces(image=image_filename)
            i += 1
            print(i, "Captured at ", current_time_to_string())
            if face_ids:
                person_ids = \
                    face_api_wrapper.identify_faces(face_ids=face_ids,
                                                    large_person_group=person_group_id)
                req_ids = [{id} for id in person_ids]
                print("Detected Faces...", req_ids)
                

            time.sleep(50)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # initial_setup()
    main()
