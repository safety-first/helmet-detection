#!/usr/bin/env python
import pika
import zmq
import random
import sys
import time
import base64
import cv2

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=localhost))
channel = connection.channel()
print("connected")
# Used as counter variable 
count = 0

# checks whether frames were extracted 
success = 1
# init the camera
camera = cv2.VideoCapture(0)  
channel.queue_declare(queue='hello')
while success: 
		# vidObj object calls read 
        success, image = camera.read()
		# function extract frames         
        frame = cv2.resize(image, (640, 480))  
 		# encode frames        
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
		# Count the frames with frame-count 
        count +=1
        print(count)
        channel.basic_publish(exchange='', routing_key='hello', body=jpg_as_text)
        print(" [x] Sent Frame %d to 'hello' queue" % count)
connection.close()

# Function to extract frames 
def FrameCapture(path): 
	
    # Path to video file 
    vidObj = cv2.VideoCapture(path) 
