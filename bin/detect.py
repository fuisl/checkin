from abc import ABC, abstractmethod

import cv2
import pyzbar

import pickle
import face_recognition


class DetectBehavior(ABC):

    @abstractmethod
    def detect(frame):
        pass

    @abstractmethod
    def draw(frame):
        pass

class FaceDetect(DetectBehavior):

    def detect(X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
        """
        Recognizes faces in given image using a trained KNN classifier

        :param X_frame: frame to do the prediction on.
        :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
        :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
        :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
            of mis-classifying an unknown person as a known one.
        :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
        """
        if knn_clf is None and model_path is None:
            raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

        # Load a trained KNN model (if one was passed in)
        if knn_clf is None:
            with open(model_path, 'rb') as f:
                knn_clf = pickle.load(f)

        X_face_locations = face_recognition.face_locations(X_frame)

        # If no faces are found in the image, return an empty result.
        if len(X_face_locations) == 0:
            return []

        # Find encodings for faces in the test image
        faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

        # Use the KNN model to find the best matches for the test face
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

        # Predict classes and remove classifications that aren't within the threshold
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


    def draw(frame, predictions):
        """
        Draw a red box and label detected faces.

        :param frame: frame to show the predictions on
        :param predictions: results of the predict function
        :return opencv suited image to be fitting with cv2.imshow fucntion:
        """

        for name, (top, right, bottom, left) in predictions:
            # enlarge the predictions for the full sized image.
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
            
            # Draw a box around the face using the Pillow module
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 3, bottom - 3), font, 1.0, (255, 255, 255), 1)

        return frame


class CodeDetect(DetectBehavior):

    def detect(frame):
        """
        Take a frame read from OpenCV, detect and return values detected as a list.

        Parameter:
        :frame: OpenCV frame
        """

        # Convert frame to gray scale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decode frame and extract codes from frame
        objs = pyzbar.decode(gray)
        
        codes = []  # initialize empty list
        for obj in objs:
            code = obj.data.decode("utf-8")  # decode data in object

            codes.append(code)

        if codes:
            return codes
    
    def draw(frame):
        """
        Draw a red box around detected QR/Barcode to the imported frame
        """
        # Convert frame to gray scale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decode frame and extract locations from frame
        objs = pyzbar.decode(gray)

        for obj in objs:
            x, y, w, h = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return frame