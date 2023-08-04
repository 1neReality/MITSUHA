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

# Install
 1. [Purchase an OpenAI API key](https://www.windowscentral.com/software-apps/how-to-get-an-openai-api-key). It's extremely affordable, since it's pay as you go, and I've been using it for a couple minutes a day like 3 times a week and I got charged less than a dollar for this month.
 2. [Install Python](https://www.python.org/downloads/) and set it as an environment variable in PATH
 3. [Download the latest release](https://github.com/DogeLord081/OneReality/releases/latest)
 4. Install WSL2 by opening a cmd in admin and running `wsl --install`
 5. Set default distro version to WSL2 with `wsl --set-default-version 2`
 6. Install [Ubuntu 22.04.2 WSL2 from Microsoft Store](https://apps.microsoft.com/store/detail/ubuntu-22042-lts/9PN20MSR04DW?hl=en-us&gl=us&rtc=1)
 7. Check that Ubuntu is WSL2 and not WSL1 by running `wsl -l -v` in cmd. If it says 1, run `wsl --set-version Ubuntu-22.04 2`
 8. In the start menu, find the app `Ubuntu 22.04.2 LTS` and open it
 9. In the terminal that pops up, run `git clone https://github.com/rhasspy/piper.git`
 10. Extract the `OneReality-main` folder from step 3 so that it is only one folder deep and rename the folder to just `OneReality`
 11. Install the Python dependencies with pip by cding into the folder and running `pip install -r requirements.txt` in cmd or powershell
 13. Add an empty text file in the OneReality-main folder called `conversation.txt`
 14. Download `model.onnx` and `model.onnx.json` from [Huggingface](https://huggingface.co/DogeLord/megumin/tree/main) and make a folder called `model` in the `OneReality` folder and put the two files in it
 15. Edit the code in `OneRealityENPublic.py` according to the comments within the code (you don't have to do anything complicated, just edit some filepaths and the OpenAI API key. Don't forget lines 154 and 185, they are the file paths to the model and output wav. /mnt/c/... means C:\... but you have to keep it as /mnt/c/... not C:\... because then WSL2 can't access it. So if the path to your model is `C:\Users\danu0\Downloads\OneReality\model9\model.onnx`, you'd make it `/mnt/c/Users/danu0/Downloads/OneReality/model9/model.onnx`)
 16. Run `OneReality.bat` and you're good to go! If you run into any issues, let me know on Discord and I might be able to help you. Once again, it's https://discord.gg/PN48PZEXJS
 17. When you want to stop, say goodbye, bye, or see you somewhere in your sentence because that automatically clears the `conversation.txt`. If you don't, it's fine you can just manually delete everything in the file

# Credits
https://github.com/ardha27/AI-Waifu-Vtuber

https://youtu.be/dKFnJCtcfMk

https://github.com/VOICEVOX/voicevox_engine
