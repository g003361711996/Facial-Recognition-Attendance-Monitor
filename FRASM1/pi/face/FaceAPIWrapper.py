import os

import cognitive_face as CF
from cognitive_face import CognitiveFaceException

from CONSTANTS import FACE_API_KEY
from utils import save_dict_to_file, current_time_to_string, load_dict_from_file

class FaceAPIWrapper:

    def __init__(self, key, base_url):
        self.key = key
        self.base_url = base_url

        CF.Key.set(self.key)
        CF.BaseUrl.set(self.base_url)


    @staticmethod
    def create_group(person_group):
        """Will Silently fail if group already exists"""
        try:
            CF.large_person_group.create(person_group)
        except CognitiveFaceException as cfe:
            print(cfe)

    @staticmethod
    def train_group(person_group):
        CF.large_person_group.train(person_group)

    @staticmethod
    def create_person(person_group, person_name):
        res = CF.large_person_group_person.create(person_group, person_name)
        person_id = res['personId']
        print("Person ID:", person_id, "| Person Name:", person_name)
        return person_id

    @staticmethod
    def add_faces_to_person(person_group, person_id, image_url):
        try:
            if os.path.isfile(image_url):
                print("Adding Image", image_url)
                persisted_face = CF.large_person_group_person_face.add(image_url,
                                                                       person_group, person_id)
               
        except CognitiveFaceException as cfe:
            print(cfe)

    @staticmethod
    def detect_faces(image):
        detected_results = CF.face.detect(image,
                                          attributes="age,gender,smile,emotion")  
        print("Detected Faces", detected_results)
        face_ids = []
        for result in detected_results:
            face_ids.append(result['faceId'])
            #json_filename = 'captured_json/' + current_time_to_string() + ".json"
            #save_dict_to_file(json_filename,detected_results)
            save_dict_to_file('attributes.json',detected_results)
            save_dict_to_file('json.txt',detected_results)
            
            #load_dict_from_file(json_filename)
        return face_ids

    @staticmethod
    def detect_face(image):
        res = CF.face.detect(image)
        return res

    @staticmethod
    def identify_faces(face_ids, large_person_group,
                       person_group_id=None, max_candidates_return=1,
                       threshold=None):
        identify_results = CF.face.identify(face_ids,
                                            large_person_group_id=large_person_group,
                                            person_group_id=person_group_id,
                                            max_candidates_return=max_candidates_return,
                                            threshold=threshold
                                            )
        person_ids = []

        for identify_result in identify_results:
            for candidate in identify_result['candidates']:
                person_id = candidate['personId']
                person_ids.append(person_id)
                #json_filename1 = 'captured_json1/' + current_time_to_string() + ".json"
                #save_dict_to_file(json_filename1,identify_result['candidates'])
                save_dict_to_file('faceId.json',person_ids)
                

        return person_ids




if __name__ == '__main__':
    main()
