import speech_recognition as sr # type: ignore
from time import ctime
import webbrowser
import os
import playsound # type: ignore
import random
from gtts import gTTS # type: ignore
import time
from bs4 import BeautifulSoup
import requests
from time import strftime

r = sr.Recognizer()

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            alexis_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            alexis_speak("Sorry, I did not get that!")
        except sr.RequestError:
            alexis_speak("Sorry my services are down!")
        return voice_data

def respond(voice_data):

    if 'news' in voice_data:
        url = 'https://www.google.com/search?q=covid-19&rlz=1C1VDKB_enIN945IN945&biw=1536&bih=722&tbm=nws&sxsrf=ALeKk01RpnIa8Iy49VuEkF8V_XiOw3yhEQ%3A1619979808514&ei=IO6OYM3zHoLhz7sPsoaA2AQ&oq=covid-19&gs_l=psy-ab.3..0l10.1022.3172.0.3509.9.7.0.2.2.0.149.751.0j6.7.0....0...1c.1.64.psy-ab..0.8.770.0...208.8r78MttMibQ'
        webbrowser.get().open(url)
        alexis_speak("Here are the latest news related to Covid 19")


    if 'search' in voice_data:
        search = record_audio('What covid related thing do you want to search for?')
        url = 'https://www.google.com/search?q='+search
        webbrowser.get().open(url)
        alexis_speak('Here is what i found for '+search)

    if 'injection' in voice_data:
        center = record_audio("Which area are you looking for?")
        url = 'https://www.google.com/search?rlz=1C1VDKB_enIN945IN945&tbs=lf:1&tbm=lcl&sxsrf=ALeKk033XGAPOmlWIYIWVucFGcZq8NQKiA:1620065867973&q=google+map+for+vaccine+centres+in+'+center+'&rflfq=1&num=10&ved=2ahUKEwjswsrUj67wAhV37HMBHVthA8cQtgN6BAgWEAo'
        webbrowser.get().open(url)
        alexis_speak("Hear are all the vaccination centres near "+center)

    if 'cases' in voice_data:
        country = record_audio("Which country are you looking for?")
        url = 'https://www.worldometers.info/coronavirus/country/'+country+'/'
        html_data = requests.get(url)
        soup = BeautifulSoup(html_data.text,'lxml')
        info_data = soup.find_all('div', id = 'maincounter-wrap')
        alexis_speak('Here are the total cases, deaths and recoveries in '+country)
        cases = info_data[0]
        alexis_speak(cases.text)
        deaths = info_data[1]
        alexis_speak(deaths.text)
        recovered = info_data[2]
        alexis_speak(recovered.text)

    if 'media' in voice_data:
        url = 'https://twitter.com/covidnewsbymib?lang=en'
        webbrowser.get().open(url)
        alexis_speak("You are on India fights Corona's official twitter page")

    if 'glide' in voice_data:
        url = 'https://covidresource.glideapp.io/'
        webbrowser.get().open(url)
        alexis_speak("Glide app has been launched for you")
        
    if 'exit' in voice_data:
        exit()


def alexis_speak(audio_string):
    tts = gTTS(text =audio_string, lang='en')
    r = random.randint(1,10000000)
    audio_file = 'audio-'+str(r)+'.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

time.sleep(1)
day_time = int(strftime('%H'))
if day_time < 12:
    alexis_speak('Good morning,My name is Alexis ')
elif 12 <= day_time < 18:
    alexis_speak('Good afternoon,My name is Alexis ')
else:
    alexis_speak('Good evening,My name is Alexis')
alexis_speak("How can I help you")

while True:
    voice_data = record_audio()
    respond(voice_data)