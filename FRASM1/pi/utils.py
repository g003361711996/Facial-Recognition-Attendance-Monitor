import datetime
import io
import os

import boto3


def preview_image(image, name="window", time=1000):
    import cv2
    cv2.imshow(name, image)
    if cv2.waitKey(time):
        cv2.destroyAllWindows()


def save_dict_to_file(file_name, dict_data):
    import json
    with open(file_name, 'w') as outfile:
        json.dump(dict_data, outfile, indent = 4, sort_keys=True)


def load_dict_from_file(file_name):
    with open(file_name) as data_file:
        import json
        data = json.load(data_file)
        print(json.dumps(data, indent = 4, sort_keys=True))
        return data


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


def current_time_to_string():
    from datetime import datetime
    return datetime.now().strftime("%H%M%S%d%m%Y")


def create_dir_if_not_exists(output_dir):
    try:
        os.makedirs(output_dir)
    except OSError:
        if not os.path.isdir(output_dir):
            raise
