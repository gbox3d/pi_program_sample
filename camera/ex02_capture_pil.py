#%%
from time import sleep
from picamera import PiCamera
from io import BytesIO
from PIL import Image

from IPython.display import display

from pkg_resources import require

print(require('picamera'))

#%%
#크기조정 
stream = BytesIO()
cam = PiCamera(
    resolution=(640,480), #해상도 지정
    framerate=30
)
print('ready..')
sleep(2)
cam.capture(stream,format='jpeg')

print(f'capture : {stream.tell()} bytes') #스트림 크기 구하기 
stream.seek(0)
image = Image.open(stream)
print(image.size)
display(image)
cam.close()

print('done')
# %%
