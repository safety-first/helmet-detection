#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import base64
import cv2

HOST_NAME = 'localhost'
QUEUE_NAME = "hello"
IMAGE_NAME = "imageToSave.png"

def callback(ch, method, properties, body):
    """
        Connection Callback.
        Decode the message as an image.
    """
    fh = open(IMAGE_NAME, "wb")
    fh.write(body.decode('base64'))
    fh.close()

    im = cv2.imread(IMAGE_NAME, -1)
    cv2.imshow("frame", im)
    if cv2.waitKey(1) == 27:
        return

if __name__ == "__main__":

    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST_NAME))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME,
                          on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()