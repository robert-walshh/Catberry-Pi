#!/usr/bin/python3
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from config import cypher_key, broker_cert
from cryptography.fernet import Fernet
from datetime import datetime
import sys
import json
def decrypt_payload(payload):
    cypher=Fernet(cypher_key)
    decrypted_payload=cypher.decrypt(payload)
    return(decrypted_payload.decode())
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))
def on_message(client, obj, msg):
    decrypted_payload=decrypt_payload(msg.payload)
    data=json.loads(decrypted_payload)
    unix_timestamp=data.get('timestamp',None)
    if unix_timestamp is not None:
     timestamp=datetime.fromtimestamp(int(unix_timestamp))
     print("Timestamp: "+str(timestamp))
    faceStatus=data.get('face spotted',None)
    if faceStatus==0:
     print("\033[31m" + "FaceSpotted: 0" + "\033[0m")
    elif faceStatus==1:
     print("\033[32m" + "FaceSpotted: 1" + "\033[0m")
    with open('facestatus.txt','w') as f:
     f.write(str(faceStatus))
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed,  QOS granted: "+ str(granted_qos))
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqttc.tls_set(broker_cert)
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# parse mqtt url for connection details
url_str = sys.argv[1]
url = urlparse(url_str)
base_topic = url.path[1:]
# Connect
if (url.username):
    mqttc.username_pw_set(url.username, url.password)
try:
    print("Connecting to "+  url_str)    
    mqttc.connect(url.hostname, url.port)
except Exception as e:
    print("Connection failed: " + str(e))
    exit(1)
# Continue the network loop, exit when an error occurs
try:  
    # Start subscribe, with QoS 1
    mqttc.subscribe(base_topic+"/#",1)
    mqttc.loop_forever()
except KeyboardInterrupt:#ctrl+c issues interrupt
    pass
finally:
    mqttc.loop_stop()
    mqttc.disconnect()
    print("Disconnected from MQTT broker.")
