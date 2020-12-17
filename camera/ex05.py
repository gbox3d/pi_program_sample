# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-to-a-network-stream
# %%
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

# %%
try:
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket = socket.socket()
    client_socket.connect(('192.168.4.208', 20834))

    # 접속승인 해더 대기  
    _welcomePacket = client_socket.recv(16)
    _checkCode, _srv_version, _extra = unpack('<LHH', _welcomePacket[0:8])

    print(f'server version {_srv_version} , checkcode {_checkCode}')

    # Make a file-like object out of the connection
    connection = client_socket.makefile('rwb')
    stream = BytesIO()

    cam = picamera.PiCamera()
    cam.resolution = (640, 480)
    print('ready..')
    sleep(2)

    while True:
        # 이미지 캡쳐
        cam.capture(stream, format='jpeg')
        # 헤더 전송
        _header = pack('<3sLB', b'jpg',
                       stream.tell(),  # 파일크기
                       0  # 버퍼 인덱스 지정(0~64)
                       )
        connection.write(_header)
        connection.flush()
        # 이미지 전송
        stream.seek(0)
        connection.write(stream.read())
        connection.flush()
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        # sleep(0.5)
finally:
    # connection.close()
    client_socket.close()
    cam.close()

# %%
