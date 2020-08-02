import cv2
from skimage import io

def detect_face(img_url):
    try:
        # Load the cascade
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Read the input image
        img = io.imread(img_url)
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        #     # Draw rectangle around the faces
        if len(faces) == 0:
            return False
        else:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Display the output
            #cv2.imshow('img', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            #cv2.waitKey()
            return True
    except:
        return False