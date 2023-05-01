import speech_recognition as sr
import openai
import os
import pydub
import pydub.playback
import io
from googletrans import Translator
import urllib
import urllib.parse
import urllib.request
import requests
import winsound
import webbrowser

print('''
  _____              ______             _ _           
 / ___ \            (_____ \           | (_)_         
| |   | |____   ____ _____) ) ____ ____| |_| |_ _   _ 
| |   | |  _ \ / _  |_____ ( / _  ) _  | | |  _) | | |
| |___| | | | ( (/ /      | ( (/ ( ( | | | | |_| |_| |
 \_____/|_| |_|\____)     |_|\____)_||_|_|_|\___)__  |
                                               (____/
        Bridging the real and virtual worlds
''')

# put your OpenAI API key here
openai.api_key = "sk-ExaMpLeeeKeY"

# set up microphone and speech recognition
r = sr.Recognizer()
mic = sr.Microphone()
r.energy_threshold = 1500

# set up OpenAI model. You can change the lore below to anything you want to give the AI whatever personality you wish
model_engine = "text-davinci-003"
lore = "You are Megumin from the anime Konosuba!. You are straightforward, lively, funny, nice, intelligent, occasionally hyper, and you have chunibyo characteristics. You are a 14 year old female Crimson Demon archwizard. The user is your creator."

# change this path to the path to your conversation.txt
chat_log = r"C:\somewhere\conversation.txt"

with open(chat_log, "r") as c:
        conversation = c.read

# define function to check if user has said "bye", "goodbye", or "see you"

def play(bytesData):
        sound = pydub.AudioSegment.from_file_using_temporary_files(io.BytesIO(bytesData))
        pydub.playback.play(sound)

def check_goodbye(transcript):
    goodbye_words = ["bye", "goodbye", "see you"]
    for word in goodbye_words:
        if word in transcript.casefold():
            return True
    return False

while True:
    print("Speak now!")
    with mic as source:
        audio = r.listen(source, timeout = 10)

    test_text = r.recognize_sphinx(audio)
    if len(test_text) == 0:
        continue
    else:
        pass

    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())

# change this path to the path to your temp.wav
    audio_file= open(r"C:\somewhere\temp.wav", "rb")
    trans = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        temperature=0.1,
        language="en"
    )

    print("You: " + trans['text'])

    words = str(trans['text'])
    with open(chat_log, "a") as c:
        c.write("\nUser:" + words)
    words = words.replace(".", "")
    words = words.lower()
    words = words.split()

# change these paths to the exes for whatever apps you want the AI to be able to open on command. You can always add or remove as many apps as you need by simply deleting or adding lines
    if len(words) > 0:
        if (words[0] == "open" or words[0] == "start"):
                app = words[1]
                if app == "youtube":
                        webbrowser.open("https://www.youtube.com/")
                elif app == "brave":
                        os.startfile(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")
                elif app == "discord":
                        os.startfile(r"C:\Users\danu0\AppData\Local\Discord\app-1.0.9012\Discord.exe")
                elif app == "spotify":
                        os.startfile(r"C:\Users\danu0\AppData\Roaming\Spotify\Spotify.exe")
                elif app == "discord":
                        os.startfile(r"C:\Windows\explorer.exe")
                elif app == "epic games":
                        os.startfile(r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe")
                elif app == "tower of fantasy":
                        os.startfile(r"C:\Tower Of Fantasy\Launcher\tof_launcher.exe")
                elif app == "steam":
                        os.startfile(r"C:\Program Files (x86)\Steam\steam.exe")
                elif app == "minecraft":
                        os.startfile(r"C:\Users\danu0\Downloads\MultiMC\MultiMC.exe")
                elif app == "clip studio paint":
                        os.startfile(r"C:\Program Files\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO\CLIPStudio.exe")
                elif app == "premiere pro":
                        os.startfile(r"C:\Program Files\Adobe\Adobe Premiere Pro 2022\Adobe Premiere Pro.exe")
                elif app == "media encoder":
                        os.startfile(r"C:\Program Files\Adobe\Adobe Media Encoder 2022\Adobe Media Encoder.exe")
                elif app == "photoshop":
                        os.startfile(r"C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe")
                elif app == "audacity":
                        os.startfile(r"C:\Program Files\Audacity\Audacity.exe")
                elif app == "obs":
                        os.chdir(r"C:\\Program Files\\obs-studio\\bin\\64bit\\")
                        os.startfile(r"obs64.exe")
                        os.chdir(r"C:\Users\danu0\Downloads\OneReality")
                elif app == "vscode":
                        os.startfile(r"C:\Program Files\VSCodium\VSCodium.exe")
                elif app == "terminal":
                        os.startfile(r"C:\Program Files\WindowsApps\Microsoft.WindowsTerminalPreview_1.17.10234.0_x64__8wekyb3d8bbwe\wt.exe")
                elif app == "synapse":
                        os.startfile(r"C:\Program Files (x86)\Razer\Synapse3\WPFUI\Framework\Razer Synapse 3 Host\Razer Synapse 3.exe")
                elif app == "via":
                        os.startfile(r"C:\Users\danu0\AppData\Local\Programs\via\VIA.exe")
                else:
                      pass
        else:
                pass
    else:
        continue
    
    if check_goodbye(trans['text']):
        c = open(chat_log, "r")

        start_sequence = "\nAI:"
        restart_sequence = "\nHuman:"

        response = openai.Completion.create(
            engine=model_engine,
            prompt=lore + "\n" + c.read(),
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            temperature=0.9,
        ).choices[0].text.strip()
        print(response)

        with open(chat_log, "a") as c:
            c.write("\n" + response)

        translator = Translator()
        response_jp = translator.translate(response, src='en', dest='ja')
        print(response_jp.text)

        global is_Speaking
        # You can change the voice to your liking. You can find the list of voices on speaker.json
        # or check the website https://voicevox.hiroshiba.jp
        params_encoded = urllib.parse.urlencode({'text': response_jp.text[5: ], 'speaker': 20})
        request = requests.post(f'http://127.0.0.1:50021/audio_query?{params_encoded}')
        params_encoded = urllib.parse.urlencode({'speaker': 20, 'enable_interrogative_upspeak': True})
        request = requests.post(f'http://127.0.0.1:50021/synthesis?{params_encoded}', json=request.json())

        with open("output.wav", "wb") as outfile:
            outfile.write(request.content)

        is_Speaking = True
        winsound.PlaySound("output.wav", winsound.SND_FILENAME)
        is_Speaking = False

        open(chat_log, "w").close()
        break

    else:
        c = open(chat_log, "r")

        start_sequence = "\nAI:"
        restart_sequence = "\nHuman:"

        response = openai.Completion.create(
            engine=model_engine,
            prompt=lore + "\n" + c.read(),
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            temperature=0.9,
        ).choices[0].text.strip()
        print(response)

        with open(chat_log, "a") as c:
            c.write("\n" + response)

        translator = Translator()
        response_jp = translator.translate(response, src='en', dest='ja')
        print(response_jp.text)

        # You can change the voice to your liking. You can find the list of voices on speaker.json
        # or check the website https://voicevox.hiroshiba.jp
        params_encoded = urllib.parse.urlencode({'text': response_jp.text[5: ], 'speaker': 20})
        request = requests.post(f'http://127.0.0.1:50021/audio_query?{params_encoded}')
        params_encoded = urllib.parse.urlencode({'speaker': 20, 'enable_interrogative_upspeak': True})
        request = requests.post(f'http://127.0.0.1:50021/synthesis?{params_encoded}', json=request.json())

        with open("output.wav", "wb") as outfile:
                outfile.write(request.content)

        is_Speaking = True
        winsound.PlaySound("output.wav", winsound.SND_FILENAME)
        is_Speaking = False