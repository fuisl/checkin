import cv2  
import os

class WebCam(object):
    def __init__(self, model_path='model/haarcascade_frontalface_default.xml', folder_image='data') -> None:
        self.video = cv2.VideoCapture(0)
        self.cascade = cv2.CascadeClassifier(model_path)
        self.counter = 0
        self.folder_image = folder_image
        
        #get width and height based on the setting of the user camera
        self.width = int(self.video.get(3))
        self.height = int(self.video.get(4))

        self.video.set(3, self.width)
        self.video.set(4, self.height)

    def __del__(self) -> None:
        self.video.release()

    def status(self) -> None:
        if not self.video.isOpened():
            print('Camera failure!')
            exit()
        else:
            print('Processing...')

    def save_data(self, frame, folder: str, user_id: str, count: int) -> str:
        '''
        Save jpg cropped image of detected face. Only used by the face_detect function. 
        Input:
            int count: the number of this frame
            frame: input cropped grayscale image
            str folder: image folder
            str user_id: user id 
        '''
        image_path = ""

        if count < 10:
            image_path = f'./{folder}/{user_id}/0{count}.jpg'
        else:
            image_path = f'./{folder}/{user_id}/{count}.jpg'

        if not os.path.isdir(f'./{folder}/{user_id}'):
            os.mkdir(f'./{folder}/{user_id}')

        cv2.imwrite(image_path, frame)

        return image_path

    def face_detect(self, frame, width: int, height: int):
        '''
        Take a normal RGB frame, convert to grayscale frame and feed to the model.
        Input:
            frame: frame read from cv2 VideoCapture
            int width: bounding box min width. Prefer measuring proportionally to the orginal input frame
            int height: bounding box min height. Prefer measuring proportionally to the orginal input frame

        Output:
            detectMultiScale2 object: coordinates of the bounding box with the following structure [(x, y, width, height), (confidence_level)]
            gray: grayscale image
        '''

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.equalizeHist(gray)

        faces = self.cascade.detectMultiScale2(
                                    hist_gray,
                                    scaleFactor=1.05,
                                    minNeighbors=10,
                                    minSize=(width,height)
                                )

        return faces, gray
    
    def gen_cam(self, user_id: str):
        '''
        Return image to the web camera and an image path if face detected. All relevant image processing units are involved here.
        '''

        ret, normal_frame = self.video.read()
        image_path = ""
    
        width = self.width
        height = self.height

        faces, gray = self.face_detect(
                            frame=normal_frame,
                            width=int(width*0.37),
                            height=int(height*0.5)
                        )
        
        #check if a face was detected
        if bool(faces[1]):
            confidence_level = faces[1][0]

            #draw bounding box
            for (x, y, w, h) in faces[0]:
                cv2.rectangle(normal_frame,(x,y),(x+w,y+h),(255,0,0),2)

            if confidence_level > 27:
                self.counter+=1

                #save and assign get image path
                image_path = self.save_data(frame=gray[y:int(y+h*1.1), int(x*0.95):int(x+w*1.1)], folder=self.folder_image, user_id=user_id, count=self.counter)

        ret, jpeg = cv2.imencode('.jpg', normal_frame)

        return jpeg.tobytes(), image_path