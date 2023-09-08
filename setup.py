import os
os.system("pip install -r requirements.txt")

import requests
import base64

cmd = os.system
# Clone the repository
cmd("git clone https://github.com/Plachtaa/VITS-fast-fine-tuning.git")

cmd("pip install cmake")

# run pip install in VITS-fast-fine-tuning directory
# if an error occurs, try to run the print to console
if cmd("pip install -r VITS-fast-fine-tuning/requirements.txt") != 0:
    print("Error occured, trying to run pip install again")
    cmd("pip install pyopenjtalk==0.1.3 --no-build-isolation --no-cache-dir")

print("Now please download an LLM model and put it in your OneReality folder. You could use https://tinyurl.com/onereality if you want.")
print("Press any key to continue after you downloaded the model.")
def wait():
    x = input("Have you downloaded a model? [y/n] ")
    if x == "y":
        print("Okay, continuing...")
    else:
        wait()
wait()

os.mkdir("model")
# URL of the file to download
url = "https://huggingface.co/DogeLord/megumin-VITS/resolve/main/G_latest.pth"

# Define the local filename where you want to save the downloaded file
local_filename = "G_latest.pth"

# Send a GET request to the URL
response = requests.get(url, stream=True)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Open a local file for binary writing
    with open("model/" + local_filename, 'wb') as file:
        # Iterate over the content in chunks and write it to the local file
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded {local_filename}")
else:
    print(f"Failed to download the file. HTTP status code: {response.status_code}")

finetune_json = "ewogICJ0cmFpbiI6IHsKICAgICJsb2dfaW50ZXJ2YWwiOiAxMCwKICAgICJldmFsX2ludGVydmFsIjogMTAwLAogICAgInNlZWQiOiAxMjM0LAogICAgImVwb2NocyI6IDEwMDAwLAogICAgImxlYXJuaW5nX3JhdGUiOiAwLjAwMDIsCiAgICAiYmV0YXMiOiBbCiAgICAgIDAuOCwKICAgICAgMC45OQogICAgXSwKICAgICJlcHMiOiAxZS0wOSwKICAgICJiYXRjaF9zaXplIjogMTYsCiAgICAiZnAxNl9ydW4iOiB0cnVlLAogICAgImxyX2RlY2F5IjogMC45OTk4NzUsCiAgICAic2VnbWVudF9zaXplIjogODE5MiwKICAgICJpbml0X2xyX3JhdGlvIjogMSwKICAgICJ3YXJtdXBfZXBvY2hzIjogMCwKICAgICJjX21lbCI6IDQ1LAogICAgImNfa2wiOiAxLjAKICB9LAogICJkYXRhIjogewogICAgInRyYWluaW5nX2ZpbGVzIjogImZpbmFsX2Fubm90YXRpb25fdHJhaW4udHh0IiwKICAgICJ2YWxpZGF0aW9uX2ZpbGVzIjogImZpbmFsX2Fubm90YXRpb25fdmFsLnR4dCIsCiAgICAidGV4dF9jbGVhbmVycyI6IFsKICAgICAgImNqa2VfY2xlYW5lcnMyIgogICAgXSwKICAgICJtYXhfd2F2X3ZhbHVlIjogMzI3NjguMCwKICAgICJzYW1wbGluZ19yYXRlIjogMjIwNTAsCiAgICAiZmlsdGVyX2xlbmd0aCI6IDEwMjQsCiAgICAiaG9wX2xlbmd0aCI6IDI1NiwKICAgICJ3aW5fbGVuZ3RoIjogMTAyNCwKICAgICJuX21lbF9jaGFubmVscyI6IDgwLAogICAgIm1lbF9mbWluIjogMC4wLAogICAgIm1lbF9mbWF4IjogbnVsbCwKICAgICJhZGRfYmxhbmsiOiB0cnVlLAogICAgIm5fc3BlYWtlcnMiOiAxLAogICAgImNsZWFuZWRfdGV4dCI6IHRydWUKICB9LAogICJtb2RlbCI6IHsKICAgICJpbnRlcl9jaGFubmVscyI6IDE5MiwKICAgICJoaWRkZW5fY2hhbm5lbHMiOiAxOTIsCiAgICAiZmlsdGVyX2NoYW5uZWxzIjogNzY4LAogICAgIm5faGVhZHMiOiAyLAogICAgIm5fbGF5ZXJzIjogNiwKICAgICJrZXJuZWxfc2l6ZSI6IDMsCiAgICAicF9kcm9wb3V0IjogMC4xLAogICAgInJlc2Jsb2NrIjogIjEiLAogICAgInJlc2Jsb2NrX2tlcm5lbF9zaXplcyI6IFsKICAgICAgMywKICAgICAgNywKICAgICAgMTEKICAgIF0sCiAgICAicmVzYmxvY2tfZGlsYXRpb25fc2l6ZXMiOiBbCiAgICAgIFsKICAgICAgICAxLAogICAgICAgIDMsCiAgICAgICAgNQogICAgICBdLAogICAgICBbCiAgICAgICAgMSwKICAgICAgICAzLAogICAgICAgIDUKICAgICAgXSwKICAgICAgWwogICAgICAgIDEsCiAgICAgICAgMywKICAgICAgICA1CiAgICAgIF0KICAgIF0sCiAgICAidXBzYW1wbGVfcmF0ZXMiOiBbCiAgICAgIDgsCiAgICAgIDgsCiAgICAgIDIsCiAgICAgIDIKICAgIF0sCiAgICAidXBzYW1wbGVfaW5pdGlhbF9jaGFubmVsIjogNTEyLAogICAgInVwc2FtcGxlX2tlcm5lbF9zaXplcyI6IFsKICAgICAgMTYsCiAgICAgIDE2LAogICAgICA0LAogICAgICA0CiAgICBdLAogICAgIm5fbGF5ZXJzX3EiOiAzLAogICAgInVzZV9zcGVjdHJhbF9ub3JtIjogZmFsc2UsCiAgICAiZ2luX2NoYW5uZWxzIjogMjU2CiAgfSwKICAic3ltYm9scyI6IFsKICAgICJfIiwKICAgICIsIiwKICAgICIuIiwKICAgICIhIiwKICAgICI/IiwKICAgICItIiwKICAgICJ+IiwKICAgICJcdTIwMjYiLAogICAgIk4iLAogICAgIlEiLAogICAgImEiLAogICAgImIiLAogICAgImQiLAogICAgImUiLAogICAgImYiLAogICAgImciLAogICAgImgiLAogICAgImkiLAogICAgImoiLAogICAgImsiLAogICAgImwiLAogICAgIm0iLAogICAgIm4iLAogICAgIm8iLAogICAgInAiLAogICAgInMiLAogICAgInQiLAogICAgInUiLAogICAgInYiLAogICAgInciLAogICAgIngiLAogICAgInkiLAogICAgInoiLAogICAgIlx1MDI1MSIsCiAgICAiXHUwMGU2IiwKICAgICJcdTAyODMiLAogICAgIlx1MDI5MSIsCiAgICAiXHUwMGU3IiwKICAgICJcdTAyNmYiLAogICAgIlx1MDI2YSIsCiAgICAiXHUwMjU0IiwKICAgICJcdTAyNWIiLAogICAgIlx1MDI3OSIsCiAgICAiXHUwMGYwIiwKICAgICJcdTAyNTkiLAogICAgIlx1MDI2YiIsCiAgICAiXHUwMjY1IiwKICAgICJcdTAyNzgiLAogICAgIlx1MDI4YSIsCiAgICAiXHUwMjdlIiwKICAgICJcdTAyOTIiLAogICAgIlx1MDNiOCIsCiAgICAiXHUwM2IyIiwKICAgICJcdTAxNGIiLAogICAgIlx1MDI2NiIsCiAgICAiXHUyMDdjIiwKICAgICJcdTAyYjAiLAogICAgImAiLAogICAgIl4iLAogICAgIiMiLAogICAgIioiLAogICAgIj0iLAogICAgIlx1MDJjOCIsCiAgICAiXHUwMmNjIiwKICAgICJcdTIxOTIiLAogICAgIlx1MjE5MyIsCiAgICAiXHUyMTkxIiwKICAgICIgIgogIF0sCiAgInNwZWFrZXJzIjogewogICAgIk1lZ3VtaW5fMSI6IDAKICB9Cn0="

with open("model/finetune_speaker.json", "w") as f:
    f.write(base64.b64decode(finetune_json).decode("utf-8"))

# print("Would you like to go through the setup here or just exit? [y/n]")
# if input() == "y":
#     print("Okay, continuing...")
# else:
#     exit()

# print("Leave any blank if you want to use the default value or if it doesn't apply to you.")
# lang = input("What language do you want to use? [Jp/En/Chi] ")
# print("--------------------")
# name = input("What is your name? ")
# print("--------------------")
# print("Go here: https://platform.openai.com/account/api-keys and click 'Create new secret key'")
# api_key = input("What is your OpenAI API key? ")
# print("--------------------")
# print("Go here: https://iot.tuya.com/cloud/basic?id=p1692112169571as54tf&region=AZ&toptab=project Access ID/Client ID is TUYA_ID and Access Secret/Client Secret is TUYA_SECRET")
# tuya_id = input("What is your TUYA_ID? ")
# tuya_secret = input("What is your TUYA_SECRET? ")
# print("In the link above, take note of the datacenter location and in this link: https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4#title-1-Endpoints find the corresponding endpoint link")
# endpoint = input("What is your endpoint link? [Leave blank for default] ")
# if endpoint == "":
#     endpoint = "https://openapi.tuyaus.com"
# print("--------------------")
# model = input("What is the name of your model file? [Leave blank for default] (wizardlm-1.0-uncensored-llama2-13b.ggmlv3.q3_K_S.bin)")
# print("--------------------")

# print("To add devices, please edit the .env file!")
print("SETUP COMPLEATE! Please edit the env file!")