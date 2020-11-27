# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-to-a-network-stream
#%%
from io import BytesIO
from struct import *
import socket
# import struct
from time import sleep
import picamera
import json

from IPython.display import display

from pkg_resources import require

print(require('picamera'))

#%%
try:
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket = socket.socket()
    client_socket.connect(('192.168.4.208', 20834))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('rwb')
    stream = BytesIO()

    cam = picamera.PiCamera()
    cam.resolution = (640, 480)
    print('ready..')
    sleep(2)

    while True:
    
        #이미지 전송
        cam.capture(stream, format='jpeg')
        print('capture frame')

        # json포멧의 헤더 전송 
        # client_socket.sendall( json.dumps({"fn": "none", "th": 0.5, "dtf": 1,"size":stream.tell()}).encode() )
        # connection.write( json.dumps({"fn": "none", "th": 0.5, "dtf": 1,"size":stream.tell()}).encode() )
        # connection.flush()
        _header = pack('<3sL',b'jpg',stream.tell())
        connection.write(_header)
        connection.flush()

        stream.seek(0)
        connection.write(stream.read())
        # connection.write(b'')
        connection.flush()


        print('send frame')

        # connection = client_socket.makefile('rb')
        # _r = connection.read()
        # print(_r)

        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        sleep(5)

finally:
    # connection.close()
    client_socket.close()
    cam.close()

# %%
