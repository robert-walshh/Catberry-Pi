import cv2
from picamera2 import Picamera2
from sense_hat import SenseHat
import time
piCam=Picamera2()
senseHat=SenseHat()
senseHat.clear()
piCam.preview_configuration.main.size=(426,240)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=15
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()
fps=0
textPos=(15,15)
font=cv2.FONT_HERSHEY_SIMPLEX
height=0.5
textColour=(0,0,255)
textWeight=1
faceCascade=cv2.CascadeClassifier('./haar_cascades/haarcascade_frontalface_default.xml')
while True:
    timeStart=time.time() # Time at Start of Loop 
    frame=piCam.capture_array()
    frame=cv2.flip(frame,-1)
    frameGrey=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # Converts Frame to Greyscale
    faces=faceCascade.detectMultiScale(frameGrey,1.3,5)
    if len(faces) > 0:
        senseHat.clear((0,255,0))
    else:
        senseHat.clear((255,0,0))
    for face in faces:
        x,y,w,h=face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
    cv2.putText(frame,'FPS '+str(int(fps)),textPos,font,height,textColour,textWeight) 
    cv2.namedWindow("piCam View",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("piCam View",720,480)
    cv2.imshow("piCam View",frame)
    if cv2.waitKey(1)==ord('q'):
       break
    timeEnd=time.time() # Time at End of Loop
    loopTime=timeEnd-timeStart # Calculate Frames per Second
    fps=.9*fps+.1*( 1/loopTime) # Filters out noisy data points
senseHat.clear()
cv2.destroyAllWindows()

