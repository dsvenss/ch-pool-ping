from picamera import PiCamera

camera = PiCamera()
# camera.rotation = 180
# camera.resolution = (2592, 1944)
# camera.framerate = 15 
#camera.start_preview(alpha=255)

# camera.start_preview()
# camera.image_effect = 'negative'
# sleep(3)
def takePicture():
    global camera
    camera.capture('current.jpg')
