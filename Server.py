# This code is on the raspberry pi used for live video streaming and qr code scanning.
# The raspberry pi is on the remote controlled drone.
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time

socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect(('192.168.43.59',8089))

print("Initializing Video Stream")
vs = VideoStream(src=0).start()
time.sleep(2.0)

found = set()

while True:
    # this part scans the qr code and writes the decoded data as a text on the frame
    frame = vs.read()
    qrcodes = pyzbar.decode(frame)
    for qrcode in qrcodes:
        (x,y,w,h) = qrcode.rect
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        qrcodeData = qrcode.data.decode("utf-8")
        text = "{}".format(qrcodeData)
        cv2.putText(frame, text, (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        if qrcodeData not in found:
            found.add(qrcodeData)
    # Serialize frame
    data = pickle.dumps(frame)
    # Send message length first
    message_size = struct.pack("L", len(data))
    # Then data
    socket.sendall(message_size + data)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
print("Quiting")
s.stop()
