import cv2
import numpy as np 
import matplotlib as plt

# img = cv2.imread('triangle.jpg', cv2.IMREAD_GRAYSCALE)
# cv2.imshow('image',img)
# cv2.waitKey(0)

cam = cv2.VideoCapture(0)

gameStarted = False
while True:
	ret,QueryImgBGR = cam.read()
	QueryImg= cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2HSV)
	Gray= cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2GRAY)
	Gray= cv2.bilateralFilter(Gray, 11, 17, 17)
	edged = cv2.Canny(Gray, 30, 200)

	cv2.imshow('edged', edged)

	(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea)[:10]
	screenCnt = None
	flag = False
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if (len(approx) == 4):
			flag = True
			screenCnt = approx
			break
	if (flag):
		if(~gameStarted):
			newy = screenCnt[0][0][1]
			gameStarted = True
		else:
			if(abs(screenCnt[0][0][1] - newy) < 50):
				newy = screenCnt[0][0][1]            
		scaledY = int(newy / 480 * 600)
		print(scaledY)



	#print(QueryImgBGR.shape[0], QueryImgBGR.shape[1])


	lower = np.array([150,150,150])
	upper = np.array([255,255,255])

	mask = cv2.inRange(QueryImgBGR, lower, upper)

	#cv2.imshow('image', QueryImgBGR)
	result = cv2.bitwise_and(QueryImgBGR, QueryImgBGR, mask=mask)

	#cv2.imshow('Result', result)

	k = cv2.waitKey(20) & 0xFF
	if (k == ord('q')):
		cam.release()
		cv2.destroyAllWindows()
		break
