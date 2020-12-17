# %%
# load module
import socket
import io
import argparse
import time
import json
import numpy as np
from struct import *
from time import sleep

from PIL import Image, ImageDraw, ImageFont
from IPython.display import display

# %%

client_socket = socket.socket()
client_socket.connect(('192.168.4.208', 20834))
client_socket.settimeout(5.0)

connection = client_socket.makefile('rwb')
buff_size = 1024

_r = client_socket.recv(16)
_checkCode,_version,_etc = unpack('<LHH',_r[0:8])

print(f'welcome checkcode {_checkCode}')

#%%
if _checkCode == 20201129 :
    print(f'connection ok server version {_version}')
    print('header data')
    _header = pack('<3sB', b'pul',0)
    connection.write(_header)
    connection.flush()

    print('wait')

    _r = client_socket.recv(buff_size)

    _checkCode,file_size = unpack('<LL',_r[0:8])

    if _checkCode == 20201129 :
        _data = _r[16:]
        while _data.__sizeof__() < file_size :
            l = client_socket.recv(buff_size)
            _data += l

        print(f'recv done {file_size} { _data.__sizeof__()}')
        if file_size > 0 :
            _img = Image.open(io.BytesIO(_data)) 
            display(_img)
        else :
            print('empty buf')
    else :
        print('invalid packet error')
#%%
client_socket.close()