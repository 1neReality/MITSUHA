# If you came here from my YouTube short, The installation is crazy so I haven't written one yet but I will probably in a couple hours or a couple days from when you read this so make sure to star it

# Demo (with VTubeStudio lip synced to Megumin)
https://youtu.be/TGZV831VTpc

# Features
- You can speak to it with a mic
- It can speak back to you in Japanese
- Has short-term memory (can remember things from the current conversation. Multi-conversation memory would take too long to respond and cost too much on the OpenAI API)
- Can open apps as long as you specify the app path in the code
- Knows everything ChatGPT does since they use pretty much the same models (ChatGPT uses the GPT-3.5-Turbo model while this uses the davinci-003 model)

# Future Features
If you think you can help with any of these or make any other improvements, join the discord and let me know please! https://discord.gg/PN48PZEXJS
- Virtual reality / augmented reality / mixed reality integration
- Making an Alexa type of thing with it, or possibly a hologram like Gatebox?
- More languages for the voice
- Mac and Linux support
- Mobile version
- Easier setup
- Compiling into one exe


# How it works
First, the Python package SpeechRecognition recognizes what you say into your mic, then that speech is written into an audio (.wav) file, which is sent to OpenAI's Whisper speech to text transcription AI, and the transcribed result is printed in the terminal and sent to OpenAI's GPT-3, then GPT's response will be printed in the terminal and translated to Japanese, which will also be printed in the terminal, and finally, the Japanese translation will be sent to the VoiceVox text to speech engine and will be read out in an anime girl-like voice. All of this happens in approximately 7-11 seconds, depending on the length of what you say, the length of what the AI says, and your GPU (slightly).

# Install (Outdated, works for Voicevox Japanese but gotta make a new tutorial for PiperTTS English soon but it's hell T-T)
[Video tutorial](https://www.youtube.com/@OneReality-tb4ut). This tutorial is for Windows only right now. I have not made any versions for Mac and Linux yet, but mabye in the future.
 1. [Purchase an OpenAI API key](https://www.windowscentral.com/software-apps/how-to-get-an-openai-api-key). It's extremely affordable, since it's pay as you go, and I've been using it for a couple minutes a day like 3 times a week and I got charged less than a dollar for this month.
 2. [Install Python](https://www.python.org/downloads/) and set it as an environment variable in PATH
 3. [Download the latest release](https://github.com/DogeLord081/OneReality/releases/latest)
 4. [Download VoiceVox Engine](https://github.com/VOICEVOX/voicevox_engine/releases/latest), if you're using an Nvidia GPU like me, click Windows（GPU/CUDA版)
  5. Extract the OneReality-main folder so that it is only one folder deep
  6. [Install 7zip](https://www.7-zip.org/download.html) and extract the VoiceVox folder so that it's also only one folder deep and drag the folder into the OneReality folder
  7. Install the Python dependencies with pip by cding into the folder and running `pip install -r requirements.txt` in cmd or powershell
  8. Edit the code in OneRealityJPPublic.py according to the comments within the code (you don't have to do anything complicated, just edit some filepaths and the OpenAI API key)
  9. Add an empty text file in the OneReality-main folder called "conversation.txt"
  10. Run OneReality.bat and you're good to go! If you run into any issues, let me know on Discord and I might be able to help you. Once again, it's https://discord.gg/PN48PZEXJS
  11. When you want to stop, say goodbye, bye, or see you somewhere in your sentence because that automatically clears the conversation.txt. If you don't, it's fine you can just manually delete everything in the file

# Credits
https://github.com/ardha27/AI-Waifu-Vtuber

https://youtu.be/dKFnJCtcfMk

https://github.com/VOICEVOX/voicevox_engine
