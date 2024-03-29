# This code lets us view the live video sent by the server as serialized frames.

import pickle
import socket
import struct
from pyzbar import pyzbar
import cv2

found = set()
HOST = socket.gethostname()
print(HOST)
HOST = socket.gethostbyname(HOST)
print(HOST)
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind(('', PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b'' 
payload_size = struct.calcsize("L") 

while True:

    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0] 

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Extract frame
    frame = pickle.loads(frame_data)
    # Display
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
