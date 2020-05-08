import time
import datetime
import io
import os
import cv2
import requests

from CONSTANTS import FACE_API_KEY, FACE_BASE_URL, CAPTURE_INTERVAL, \
    REST_SERVER_URL, FACE_GROUP_ID, CAMERA_NAME
from camera.Camera import Camera
from face.FaceAPIWrapper import FaceAPIWrapper
from utils import get_lecture_number, upload_to_s3, current_time_to_string, create_dir_if_not_exists


def main():
    person_group_id = 'students'
    display_image = False

    face_api_wrapper = FaceAPIWrapper("##MY_KEY###", 'https://projectface.cognitiveservices.azure.com/face/v1.0')
    create_dir_if_not_exists('capturedImages/' + "Camera 1")
    print("Capture Image every ", 60, " seconds...")

    i = 0

    while 1:
        try:
            image_filename = 'capturedImages/' + "Camera 1" + "/" + current_time_to_string() + ".jpg"
            image = Camera().capture_image()
            cv2.imwrite(image_filename, image)

            if display_image:
                cv2.imshow("Camera Image", image)
                cv2.waitKey(1)

            image_link = upload_to_s3(image_filename)
            face_ids = face_api_wrapper.detect_faces(image=image_filename)
            i += 1
            print(i, "Captured at ", time.time())
            if face_ids:
                person_ids = \
                    face_api_wrapper.identify_faces(face_ids=face_ids,
                                                    large_person_group=person_group_id)
                req_ids = [{id} for id in person_ids]
                print("Detected Faces...", req_ids

            time.sleep(60)
        except Exception as e:
            print(e)



if __name__ == '__main__':
    # initial_setup()
    main()
                      
def current_time_to_string():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S%f")

def upload_to_s3(key):
    print("Uploading file to S3...")
    bucket_name = 'mybuckfucket'

    folder_name = "public_folder"
    output_name = folder_name + "/" + key
    location = 'us-west-1'

    s3 = boto3.client('s3')
    s3.upload_file(key, bucket_name, output_name, ExtraArgs={'ACL': 'public-read'})

    url = "https://s3.amazonaws.com/%s/%s/%s" % (bucket_name, folder_name, key)
    return url
                      

def create_dir_if_not_exists(output_dir):
    try:
        os.makedirs(output_dir)
    except OSError:
        if not os.path.isdir(output_dir):
            raise