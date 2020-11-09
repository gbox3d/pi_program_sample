from time import sleep
from picamera import PiCamera

#v2 3280x2464
#v1 2592x1944

camera = PiCamera()
camera.resolution = (2592,1944) #크기지정 
print('ready...')
sleep(2)
print('capturing...')
camera.capture('foo.jpg')
print('done!')
