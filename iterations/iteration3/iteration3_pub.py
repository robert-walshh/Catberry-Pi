#!/usr/bin/python3
import cv2
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from picamera2 import Picamera2
from sense_hat import SenseHat
from cryptography.fernet import Fernet
from config import cypher_key,broker_cert
import sys
import time
import json
import schedule
piCam=Picamera2()
senseHat=SenseHat()
mqttc=mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqttc.tls_set(broker_cert)
senseHat.clear()
def encrypt_payload(payload):
    cypher=Fernet(cypher_key)
    encrypted_payload=cypher.encrypt(payload.encode('utf-8'))
    return(encrypted_payload.decode())
def on_connect(client,userdata,flags,rc):
    print("Connection Result: " + str(rc))
def on_publish(client,obj,mid):
    print ("Message ID: " + str(mid))
mqttc.on_connect=on_connect
mqttc.on_publish=on_publish
url_str=sys.argv[1]
print(url_str)
url=urlparse(url_str)
base_topic=url.path[1:]
if (url.username):
    mqttc.username_pw_set(url.username,url.password)
try:
    print("Connecting to "+ url_str)
    mqttc.connect(url.hostname,url.port)
    mqttc.loop_start()
except Exception as e:
    print("Connection failed: " + str(e))
    exit(1)
piCam.preview_configuration.main.size=(426,240)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=15
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()
faceSpotted=0
faceCascade=cv2.CascadeClassifier('./haar_cascades/haarcascade_frontalface_default.xml')
def publish_faceStatus():
    face_json=json.dumps({"face spotted":faceSpotted, "timestamp":time.time()})
    mqttc.publish(base_topic+"/face spotted",encrypt_payload(face_json),1)
schedule.every(1).seconds.do(publish_faceStatus)
while True:
    frame=piCam.capture_array()
    frame=cv2.flip(frame,-1)
    frameGrey=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # Converts Frame to Greyscale
    faces=faceCascade.detectMultiScale(frameGrey,1.3,5)
    if len(faces) > 0:
        senseHat.clear((0,255,0))
        faceSpotted=1
    else:
        senseHat.clear((255,0,0))
        faceSpotted=0
    for face in faces:
        x,y,w,h=face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
    cv2.namedWindow("piCam View",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("piCam View",720,480)
    cv2.imshow("piCam View",frame)
    if cv2.waitKey(1)==ord('q'):
        break
    schedule.run_pending()
    time.sleep(1)
senseHat.clear()
mqttc.loop_stop()
mqttc.disconnect()
print("The fun is over... goodbye!!!")
cv2.destroyAllWindows()
