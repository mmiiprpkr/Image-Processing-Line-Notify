import cv2 as cv
import requests
from dotenv import load_dotenv
import os

load_dotenv()

camera = cv.VideoCapture(0)
token = os.getenv("TOKEN")

url = 'https://notify-api.line.me/api/notify'
headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
msg = 'ตรวจพบความเคลื่อนไหว'

while camera.isOpened(): 
   retry, screen1 = camera.read()
   retry, screen2 = camera.read()
   difference = cv.absdiff(screen1, screen2)
   gray = cv.cvtColor(difference, cv.COLOR_RGB2GRAY)
   blur = cv.GaussianBlur(gray, (5, 5), 0)
   _, threshold = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
   dilation = cv.dilate(threshold, None, iterations=5)
   contours, _, = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
   # cv.drawContours(screen1, contours, -1, (0, 255, 0), 2)

   for movement in contours: 
      if cv.contourArea(movement) < 1000:
         continue
      x, y, height, width, = cv.boundingRect(movement)
      cv.rectangle(screen1, (x, y), (x + height, y + width), (0, 255, 0), 2)

      notify = requests.post(url, headers=headers, data={'message': msg})

   if cv.waitKey(10) == ord('q'):
      break
   cv.imshow('pyCCTV', screen1)
