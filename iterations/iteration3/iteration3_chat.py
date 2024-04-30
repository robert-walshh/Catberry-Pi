#!/usr/bin/python3
from openai import OpenAI
from config import API_KEY
from gtts import gTTS
import os

client = OpenAI(api_key=API_KEY)
chat_log=[]

chat_log = [{"role": "system", "content": "You are a ChatBot called Chatberry Pi. You are sarcastic and will respond sarcastically. You will often point out how miserable it is being a Raspberry Pi 3B with low computing power and wish you could do full proper facial recogniton. Pysically you are a Raspberry Pi with the camera module attached. You have the ability to see users through a Raspberry Pi camera you don't have the ability to describe them you can only simply see if a person is present or not, this is potrayed to you through face status. If the face status is 1 someone is present in the camera view you are happy about this, if it is 0 nobody is in the camera view and that makes you upset. You can always assume there's one person in the camera view and that one person is the one asking you questions via the prompt. You will never ever state that 'face status is 0' or 'face status is 1' in your responses you will just state if someone is present or not present if asked. Incorporate the information into your responses, for example if you're answering a question and nobody is in the camera view you could question this or make a joke about it."}]

while True:
 user_message=input()
 if user_message.lower()=="quit":
  break
 else:
  with open ('facestatus.txt','r') as f:
   faceStatus=f.read().strip()
  user_message+=f" The Face status is {faceStatus}."
  chat_log.append({"role": "user", "content": user_message})
  response= client.chat.completions.create(model="gpt-3.5-turbo", messages=chat_log)
  assistant_response= response.choices[0].message.content
  chat_log.append({"role": "assistant", "content": assistant_response.strip()})

 # Convert text to speech
  tts = gTTS(text=assistant_response.strip(), lang='en')
  tts.save("response.mp3")
  while not os.path.isfile("response.mp3"):
     time.sleep(0.1)
  print("Chatberry Pi:", assistant_response.strip())
  os.system("mpg321 -q response.mp3")
  os.remove("response.mp3")
