import datetime
import os
import random
import smtplib
import sys
import webbrowser
import cv2
import pyautogui
import pyttsx3
import pywhatkit as kit
import speech_recognition as sr
import wikipedia
import requests
from requests import get
import pyjokes
import time
import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis import Ui_Jarvis

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voices', voices[0].id)

# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# To convert voice into text
def takecommand(self):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=9, phrase_time_limit=9)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}")

    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query

# to wish
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am jarvis sir , please tell me how can i help you")


# to send email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('***********@gmail.com', '*************@123')
    server.sendmail(",,,,,,,,,,,,,,,,,.com", to, content)
    server.close()


def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=eeb08bf875db44f02ace04ee9746f5c62'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "Third", "Fourth", "Fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()    

   
    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
           
            audio = r.listen(source, timeout=9, phrase_time_limit=9)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")

        except Exception as e:
            speak("Say that again please...")
            return "none"
        return query

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand()

            # logic building for tasks

            if "open Notepad" in self.query:
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif "open telegram"  in self.query:
                tpath = "D:\\Telegram Desktop\\Telegram.exe"
                os.startfile(tpath)

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(60)
                    if k==27:
                        break;
                    cap.release()
                    cv2.destroyAllWindows()

            elif "play music" in self.query:
                music_dir = "C:\\Users\\Hemanth\\Desktop\\Jarvis\\Music FIles"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif "IP address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "Wikipedia" in self.query:
                speak("searching wikipedia....")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("according to Wikipedia")
                speak(results)
                print(results)

            elif "open Youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open Facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "open Google" in self.query:
                speak("Sir , what should i search on google")
                cm = takecommand(self).lower()
                webbrowser.open(f"{cm}")

            elif "send a message" in self.query:
                kit.sendwhatmsg("+91********", "testing whatsapp", 6, 56)


            elif "song on YouTube" in self.query:
                kit.playonyt("see you again")

            elif "send email to me" in self.query:
                try:
                    speak("what should i say")
                    content = self.takecommand().lower()
                    to = "...........@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent")

                except Exception as e:
                    print(e)
                    speak("sorry sir not able to send email")

            elif "no thanks" in self.query:
                speak("thanks for using me sir, have a good day.")
                sys.exit()

            elif "close notepad" in self.query:
                speak("okay sir, closing notepad")
                os.system("taskkill /f /im notepad.exe")

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "switch the window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "tell me news" in self.query:
                speak("please wait sir, fetching the latest news")
                news()

            elif "where I am" in self.query or "where are we" in self.query:
                speak("wait sir, let me check")
                try:
                    r = requests.get('https://get.geojs.io/')

                    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
                    ipAdd = ip_request.json()['ip']
                    print(ipAdd)

                    url = 'https://get.geojs.io/v1/ip/geo/'+'115.96.77.21'+'.json'
                    geo_request = requests.get(url)
                    geo_data = geo_request.json()
                    speak(geo_data)
                except Exception as e:
                    speak("sorry sir, Due to network issues i think i am not able to find where we are.")
                    pass



            speak("sir, do you have any other work?")

    


# class MainThread:
    # pass

#class MainThread(QThread):
  #  def __init__(self):
   #     super(MainThread,self).__init__()
    
  #  def run(self):
 #      self.TaskExcecution(self)



startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Jarvis()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\Hemanth\\Desktop\\jarvisgui\\../Jarvis/jarvis 4.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:\\Users\\Hemanth\\Desktop\\jarvisgui\\../Jarvis/jarvis 3.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis1 = Main()
jarvis1.show()
exit(app.exec_())

