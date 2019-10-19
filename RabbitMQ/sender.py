#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author  : Mustafa Durmuş [mustafa-durmuss@outlook.com]

import pika
import base64
import cv2

HOST_NAME = 'localhost'
QUEUE_NAME = "hello"


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST_NAME))
    channel = connection.channel()
    print("connected")
    
    count = 0                    # Used as counter variable
    success = 1                  # checks whether frames were extracted
    camera = cv2.VideoCapture(0) # init the camera
    
    channel.queue_declare(queue=QUEUE_NAME)
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
            channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=jpg_as_text)
            print(" [x] Sent Frame %d to 'hello' queue" % count)
    connection.close()

if __name__ == "__main__":
    main()