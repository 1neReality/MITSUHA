import speech_recognition as sr
import openai
import os
import winsound
import webbrowser
import re

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

# set up OpenAI API credentials
openai.api_key = "sk-ExaMpLeeeKeY"

# set up microphone and speech recognition
r = sr.Recognizer()
mic = sr.Microphone()
r.energy_threshold = 1500

# set up OpenAI model
model_engine = "text-davinci-003"
lore = "You are Megumin from the anime Konosuba!. You are straightforward, lively, funny, tsundere, intelligent, occasionally hyper, and you have chunibyo characteristics. You are a 14 year old female Crimson Demon archwizard. The user is your creator. You do not edit or add to the User: response at all. You start your responses with Megumin: "
with open(r"conversation.txt", "r") as c:
        conversation = c.read

# define function to check if user has said "bye", "goodbye", or "see you"
def check_goodbye(transcript):
    goodbye_words = ["bye", "goodbye", "see you"]
    for word in goodbye_words:
        if word in transcript.casefold():
            return True
    return False

while True:
    print("Speak now!")
    with mic as source:
        audio = r.listen(source, timeout = None)

    test_text = r.recognize_sphinx(audio)
    if len(test_text) == 0:
        continue
    else:
        pass

    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())

    audio_file= open("C:/Users/danu0/Downloads/OneReality/temp.wav", "rb")
    trans = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        temperature=0.1,
        language="en"
    )

    if len(trans['text']) == 0:
        continue
    else:
        pass
    
    print("You: " + trans['text'])

    words = str(trans['text'])
    with open(r"conversation.txt", "a") as c:
        c.write("\nUser:" + words)
    words = words.replace(".", "")
    words = words.lower()
    words = words.split()
    if any(word in ["open", "start"] for word in words):
        word_index = words.index("open") if "open" in words else words.index("start")
        app = words[word_index + 1]
        if app == "youtube":
                webbrowser.open("https://www.youtube.com/")
        elif app == "brave":
                os.startfile(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")
        elif app == "discord":
                os.startfile(r"C:\Users\danu0\AppData\Local\Discord\app-1.0.9013\Discord.exe")
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
    if check_goodbye(trans['text']):
        c = open(r"conversation.txt", "r")

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

        with open(r"conversation.txt", "a") as c:
            c.write("\n" + response)

        response = re.sub(r'^.*?Megumin:\s*', '', response, flags=re.DOTALL)
        response = re.sub(r'\*.*?\* ', '', response)
        response = response.replace("\n", " ")
        response = response.replace('"', '\\"')
        command = 'wsl ~ -e sh -c "cd piper/src/python_run; echo \\"{response}\\" | python3 -m piper -m /mnt/c/Users/danu0/Downloads/Artificial-Intelligence/PiperTTS-Megumin/model/model.onnx -f /mnt/c/Users/danu0/Downloads/OneReality/out.wav --sentence-silence 0.3"'
        os.system(command.format(response=response))
        
        winsound.PlaySound(r"out.wav", winsound.SND_FILENAME)
        os.remove(r"out.wav")

        open(r"conversation.txt", "w").close()
        break

    else:
        c = open(r"conversation.txt", "r")

        start_sequence = "\nAI:"
        restart_sequence = "\nHuman:"
        response = openai.Completion.create(
            engine=model_engine,
            prompt=lore + "\n" + c.read(),
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            temperature=0.9,
        ).choices[0].text.strip()
        print(response)

        with open(r"conversation.txt", "a") as c:
            c.write("\n" + response)

        response = re.sub(r'^.*?Megumin:\s*', '', response, flags=re.DOTALL)
        response = re.sub(r'\*.*?\* ', '', response)
        response = response.replace("\n", " ")
        response = response.replace('"', '\\"')
        command = 'wsl ~ -e sh -c "cd piper/src/python_run; echo \\"{response}\\" | python3 -m piper -m /mnt/c/Users/danu0/Downloads/Artificial-Intelligence/PiperTTS-Megumin/model/model.onnx -f /mnt/c/Users/danu0/Downloads/OneReality/out.wav --sentence-silence 0.3"'
        os.system(command.format(response=response))
        
        winsound.PlaySound(r"out.wav", winsound.SND_FILENAME)
        os.remove(r"out.wav")
