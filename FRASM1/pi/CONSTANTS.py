import os

CAMERA_PORT = 0
IS_RASPBERRY_PI = True
RESOLUTION_H = 1640
RESOLUTION_W = 922
CAPTURE_INTERVAL = 15
GPIO_SWITCH = 24

IMAGE_PATH = 'captured_images/'
CAMERA_NAME = os.environ.get('CAMERA_NAME', "Camera1")

FACE_API_KEY = os.environ.get('FACE_API_KEY', "fc36b866a9c84de3bdc3c29df2b7705c")

FACE_BASE_URL = 'https://projectface.cognitiveservices.azure.com/face/v1.0'

FACE_GROUP_ID = 'students'

REST_SERVER_URL = os.environ.get('REST_SERVER_URL', 'http://127.0.0.1:8000/')
