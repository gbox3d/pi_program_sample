#%%
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image

from IPython.display import display

from pkg_resources import require

print( f'picamera version : {require("picamera")[0].version}')

#%%
#비압축(raw) 비트멥 , numpy 형식의 배열사용예 
IM_WIDTH = 640
IM_HEIGHT = 480

cam = PiCamera(
    resolution=(640,480), #해상도 지정
    framerate=2
)
rawCapture = PiRGBArray(cam, size=(IM_WIDTH, IM_HEIGHT))
rawCapture.truncate(0)

print('ready..')
sleep(2)
cam.capture(rawCapture,format='rgb')

# print(f'capture : {stream.tell()} bytes') #스트림 크기 구하기 
# print(rawCapture)

image = Image.fromarray(rawCapture.array)
print(image.size)
display(image)
cam.close()

print('done')
# %%
