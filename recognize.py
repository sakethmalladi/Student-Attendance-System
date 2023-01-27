# URL - https://www.pyimagesearch.com/2018/09/24/opencv-face-recognition/
# USAGE
# python recognize.py --detector face_detection_model \
# 	--embedding-model openface_nn4.small2.v1.t7 \
# 	--recognizer output/recognizer.pickle \
# 	--le output/le.pickle --image images/adrian.jpg

# import the necessary packages
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
passw='Arunamalladi!'

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-sub", "--subject", type=str,required=True)
args = vars(ap.parse_args())
# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())

# load the image, resize it to have a width of 600 pixels (while
# maintaining the aspect ratio), and then grab the image dimensions
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)
(h, w) = image.shape[:2]

# construct a blob from the image
imageBlob = cv2.dnn.blobFromImage(
	cv2.resize(image, (300, 300)), 1.0, (300, 300),
	(104.0, 177.0, 123.0), swapRB=False, crop=False)

# apply OpenCV's deep learning-based face detector to localize
# faces in the input image
detector.setInput(imageBlob)
detections = detector.forward()
li=[]
# loop over the detections
for i in range(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]

	# filter out weak detections
	if confidence > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for the
		# face
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		# extract the face ROI
		face = image[startY:endY, startX:endX]
		(fH, fW) = face.shape[:2]

		# ensure the face width and height are sufficiently large
		if fW < 20 or fH < 20:
			continue

		# construct a blob for the face ROI, then pass the blob
		# through our face embedding model to obtain the 128-d
		# quantification of the face
		faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
			(0, 0, 0), swapRB=True, crop=False)
		embedder.setInput(faceBlob)
		vec = embedder.forward()

		# perform classification to recognize the face
		preds = recognizer.predict_proba(vec)[0]
		j = np.argmax(preds)
		proba = preds[j]
		names = le.classes_[j]
		li.append(names)

print(li)
import pymysql
from datetime import date
#if
today = date.today() 
db = pymysql.connect("localhost","root",passw,"attendance" )
cursor = db.cursor()
sql="select Date from class where Date=('%s')" % (today);
try:
   cursor.execute(sql)
   db.commit()
except:
   db.rollback()
rows=cursor.fetchall()
print(rows)
if len(rows)==0:
	sql = "INSERT INTO class VALUES ('%s','%s','%s','%s')" % (today,'{"s1": "y1","s2": "y2","s3": "y3","s4": "y4","s5": "y5","s6": "y6"}','{"s1": "y1","s2": "y2","s3": "y3","s4": "y4","s5": "y5","s6": "y6"}','{"s1": "y1","s2": "y2","s3": "y3","s4": "y4","s5": "y5","s6": "y6"}')
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	print("executed")
	#sql3 = "INSERT INTO class(s2) VALUES ('%s')" % ('{"s1": "y1","s2": "y2","s3": "y3","s4": "y4","s5": "y5","s6": "y6"}')
	
sub=args["subject"]
for i in range(len(li)):
	qw='"$.'+li[i]+'"'
	s="update class set "+sub+"=json_set("+sub+","+qw+",'yes')"

	s = s+" WHERE Date = '%s'" % (today)
	print(s)

	try:
	   cursor.execute(s )
	except:
	   db.rollback()

db.commit()
db.close()