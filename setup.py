print('''
  _____              ______             _ _           
 / ___ \            (_____ \           | (_)_         
| |   | |____   ____ _____) ) ____ ____| |_| |_ _   _ 
| |   | |  _ \ / _  |_____ ( / _  ) _  | | |  _) | | |
| |___| | | | ( (/ /      | ( (/ ( ( | | | | |_| |_| |
 \_____/|_| |_|\____)     |_|\____)_||_|_|_|\___)__  |
                                               (____/
        Bridging the real and virtual worlds
                [Install Script]
''')

import os

x = input("Are you on windows and have an Nvidia GPU? [windows/linux/neither] ")
if x == "windows":
  print("Okay, installing pytorch with CUDA 11.7...")
  os.system("pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117")
elif x == "linux":
  print("Okay, installing pytorch with CUDA 11.7...")
  os.system("pip3 install torch torchvision torchaudio")
elif x == "neither":
  print("If you're on Mac or don't have an Nvidia GPU, unfortunately you cannot use GPU mode. Continuing with CPU...")
  
os.system("pip install -r requirements.txt")

import requests
import base64
import time

cmd = os.system

cmd("pip install cmake")

# run pip install in VITS-fast-fine-tuning directory
# if an error occurs, try to run the print to console
cmd("pip install cython")

print("Now please download an LLM model and put it in your OneReality folder. I suggest WizardLM https://tinyurl.com/onereality which is what I use.")
print("Press any key to continue after you downloaded the model.")
def wait():
    x = input("Have you downloaded a model and put it in the OneReality folder? [y/n] ")
    if x == "y":
        print("Okay, continuing...")
    else:
        wait()
wait()


# URL of the file to download
url = "https://huggingface.co/DogeLord/megumin-VITS/resolve/main/G_latest.pth"

# Define the local filename where you want to save the downloaded file
local_filename = "G_latest.pth"

# Send a GET request to the URL
response = requests.get(url, stream=True)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Open a local file for binary writing
    with open("vits-simple-api-onereality/Model/g/" + local_filename, 'wb') as file:
        # Iterate over the content in chunks and write it to the local file
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded {local_filename}")
else:
    print(f"Failed to download the file. HTTP status code: {response.status_code}")

print("Do you want to use tuya? (Basically smart home control with the AI but a bit complicated to set up. Check the prerequisites on my README on my Github.) [y/n]")
if input() == "n":
    print("Okay, Removing tuya from script...")
else:
    print("Okay, continuing...")
    

    
with open ("OneRealityMemory.py", "r") as f:
    data = f.read()
    data = data.replace("tuya = True", "tuya = False")
    
with open ("OneRealityMemory.py", "w") as f:
    f.write(data)
    
print("If you want to use tuya, please edit the OneRealityENMemory.py file! and set tuya = True")
print("SETUP COMPLEATE! Please edit the env file!")
print("Note if you encounter any errors when running OneReality.bat, please read the error, it might say install this or that. if you can't figure it out, please contact me on discord: https://discord.gg/PN48PZEXJS")


print("Would you like to go through the setup here or just exit? ONLY RUN THIS ONCE! [y/n]")
print("If you want to change anything after the first time, please edit the .env file!")
if input() == "y":
    print("Okay, continuing...")
else:
    exit()

print("Leave any blank if you want to use the default value or if it doesn't apply to you, like if you aren't using Tuya.")
print("--------------------")
print("Supported languages are: English, 한국어, 日本語, or 简体中文")
language = input("What language do you want to use? ")
print("--------------------")
name = input("What is your name? ")
print("--------------------")
print("Go here: https://platform.openai.com/account/api-keys and click 'Create new secret key'")
api_key = input("What is your OpenAI API key? ")
print("--------------------")
print("Go here: https://iot.tuya.com/cloud/basic?id=p1692112169571as54tf&region=AZ&toptab=project Access ID/Client ID is TUYA_ID and Access Secret/Client Secret is TUYA_SECRET")
tuya_id = input("What is your TUYA_ID? ")
tuya_secret = input("What is your TUYA_SECRET? ")
print("In the link above, take note of the datacenter location and in this link: https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4#title-1-Endpoints find the corresponding endpoint link")
endpoint = input("What is your endpoint link? [Leave blank for default] ")
if endpoint == "":
    endpoint = "https://openapi.tuyaus.com"
print("--------------------")
model = input("What is the name of your model file? [Leave blank for default] (wizardlm-1.0-uncensored-llama2-13b.ggmlv3.q3_K_S.bin)")
print("--------------------")

print("To add Tuya devices, please edit the .env file!")

# Now we need to write the data to the env file
with open(".env", "r") as f:
    data = f.read()
    data = data.replace("LANGUAGE", language)
    data = data.replace("NAME", name)
    data = data.replace("APIKEY", api_key)
    data = data.replace("TUYAID", tuya_id)
    data = data.replace("TUYASECRET", tuya_secret)
    data = data.replace("https://openapi.tuyaus.com", endpoint)
    if not model == "":
        data = data.replace("wizardlm-1.0-uncensored-llama2-13b.ggmlv3.q3_K_S.bin", model)
        
with open(".env", "w") as f:
    f.write(data)
    
print("SETUP COMPLEATE! Please edit the env file if you need to add Tuya devices or if you want to change anything else! Thanks for using OneReality!")
