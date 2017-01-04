#image_batch_resize.py
# Isolates face images found by OpenCV's cascade classifier into
# into identically sized smaller images for ML training use
import os
import cv2
import numpy as np

#Path to root directory of this file
root_dir = os.path.dirname(os.path.realpath(__file__))

#Location of sub images to be extracted
image_folder = root_dir + "/training_images/pos/"

#Default face haar cascade file
face_cascade = cv2.CascadeClassifier(root_dir + "/cascades/haarcascade_frontalface_default.xml")

#Resize dimension
r_dim = (30, 30)

for file in os.listdir(image_folder):
	#Import current image
    img = cv2.imread(image_folder + file)

	#Convert image to grayscale before searching for faces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Find faces in image
    faces = face_cascade.detectMultiScale(gray,1.3,5)

	#Isolate, resize, and save each face sub-image. Using index to append to new filenames
    for index, (x, y, w, h) in enumerate(faces):
		#Crop current face into sub image (img[lowerleft y: y + height, lowerleft x: x + w])
        sub_face_img = img[y:y+h,x:x+w]

		#Resize current face image to desired size for ML classifier training
        scaled_face = cv2.resize(sub_face_img, r_dim)

		#Current face img location/filename
        face_title = root_dir + "/faces/pos/" + file[:-4] + "_face_" + str(index) +".jpg"

		#Save isolated image to new file
        cv2.imwrite(face_title, scaled_face)