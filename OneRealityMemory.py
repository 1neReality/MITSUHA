import speech_recognition as sr
import os
import sounddevice as sd
import soundfile as sf
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tuya_connector import TuyaOpenAPI
import string
from AppOpener import open as start, close as end
import json
from vectordb import Memory
from dotenv import load_dotenv
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from datetime import datetime
import whisperx
import pyautogui
import time
import subprocess

subprocess.Popen("start cmd /k python vits-simple-api-onereality/app.py", shell=True)
###
# Set to True if you want to use tuya
tuya = True
###

# Load env variables
load_dotenv()

# Language
lang_code = os.getenv("LANGUAGE")

# Initialize memory
memory = Memory()


with open("conversation.jsonl", "r", encoding="utf-8") as f:
    conversation_data = [json.dumps(json.loads(line)) for line in f]
memory.save(conversation_data)

# ExLlamaV2
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer,
)

from exllamav2.generator import ExLlamaV2StreamingGenerator, ExLlamaV2Sampler

# Initialize model and cache

model_directory = os.getenv("LLM_PATH")

config = ExLlamaV2Config()
config.model_dir = model_directory
config.prepare()


ExLlamatokenizer = ExLlamaV2Tokenizer(config)
model = ExLlamaV2(config)
print("Loading model: " + model_directory)
model.load([16, 24])

cache = ExLlamaV2Cache(model)

# Initialize generator

generator = ExLlamaV2StreamingGenerator(model, cache, ExLlamatokenizer)
generator.set_stop_conditions(['"}', "}", "'}"])

# Settings

settings = ExLlamaV2Sampler.Settings()
settings.temperature = 0.85
settings.top_k = 50
settings.top_p = 0.8
settings.token_repetition_penalty = 1.15
settings.disallow_tokens(ExLlamatokenizer, [ExLlamatokenizer.eos_token_id])

max_new_tokens = 1000

# WhisperX
device = "cuda"
audio_file = r"temp.wav"
batch_size = 12  # reduce if low on GPU mem
compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)
language = lang_code
model = os.getenv("WHISPERX_MODEL")

whisper_model = whisperx.load_model(
    "medium",
    device,
    language=language,
    compute_type=compute_type,
    asr_options={
        "initial_prompt": "A chat between a user and an artificial intelligence assistant named M.I.T.S.U.H.A."
    },
)

# VITS api
abs_path = os.path.dirname(__file__)
base = "http://127.0.0.1:23456"

if tuya == True:
    # set up Tuya API credentials
    ACCESS_ID = os.getenv("TUYA_ID")
    ACCESS_KEY = os.getenv("TUYA_SECRET")
    API_ENDPOINT = os.getenv("TUYA_ENDPOINT")

# set up microphone and speech recognition
r = sr.Recognizer()
mic = sr.Microphone()
r.energy_threshold = 1500

# set up NLI RTE transformers model
tokenizer = AutoTokenizer.from_pretrained(os.getenv("NLI_RTE_TRANSFORMER"))
model = AutoModelForSequenceClassification.from_pretrained(
    os.getenv("NLI_RTE_TRANSFORMER")
)

# set up Llama model
lore = os.getenv("LORE")

print(
    """
  _____              ______             _ _           
 / ___ \            (_____ \           | (_)_         
| |   | |____   ____ _____) ) ____ ____| |_| |_ _   _ 
| |   | |  _ \ / _  |_____ ( / _  ) _  | | |  _) | | |
| |___| | | | ( (/ /      | ( (/ ( ( | | | | |_| |_| |
 \_____/|_| |_|\____)     |_|\____)_||_|_|_|\___)__  |
                                               (____/
"""
)


def typewriter_effect(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)


text = """        Bridging the real and virtual worlds
{:^50}
""".format(
    "[PROJECT M.I.T.S.U.H.A.]"
)

typewriter_effect(text)


# tts function
def voice_vits(
    text, id=0, format="wav", lang=lang_code, length=1, noise=0.667, noisew=0.8, max=50
):
    fields = {
        "text": text,
        "id": str(id),
        "format": format,
        "lang": lang,
        "length": str(length),
        "noise": str(noise),
        "noisew": str(noisew),
        "max": str(max),
    }
    boundary = "----VoiceConversionFormBoundary" + "".join(
        random.sample(string.ascii_letters + string.digits, 16)
    )

    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{base}/voice"

    res = requests.post(url=url, data=m, headers=headers)
    path = f"{abs_path}/out.wav"

    with open(path, "wb") as f:
        f.write(res.content)
    print(path)
    return path


# define function to check if user has said "bye", "goodbye", or "see you"
def check_goodbye(transcript):
    goodbye_words = ["bye", "goodbye", "see you"]
    for word in goodbye_words:
        if word in transcript.casefold():
            return True
    return False


def test_entailment(text1, text2):
    batch = tokenizer(text1, text2, return_tensors="pt").to(model.device)
    with torch.no_grad():
        proba = torch.softmax(model(**batch).logits, -1)
    return proba.cpu().numpy()[0, model.config.label2id["ENTAILMENT"]]


def test_equivalence(text1, text2):
    return test_entailment(text1, text2) * test_entailment(text2, text1)


def replace_device(sentence, word):
    return sentence.replace("[device]", word)


def replace_app(sentence, word):
    return sentence.replace("[app]", word)


def keep_sentence_with_word(text, word):
    sentences = text.split(".")
    filtered_sentences = [
        sentence.strip() + "." for sentence in sentences if word in sentence
    ]
    result = " ".join(filtered_sentences)
    return result


def keep_sentence_with_word(text, word):
    sentences = re.split(r"[.,!?]", text)
    filtered_sentences = [
        sentence.strip() + punct
        for sentence, punct in zip(sentences, re.findall(r"[.,!?]", text))
        if word in sentence
    ]
    result = " ".join(filtered_sentences)
    return result


while True:
    print("Speak now!")

    with mic as source:
        audio = r.listen(source, timeout=None)

    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time_2 = now.strftime("%H:%M:%S")

    try:
        test_text = r.recognize_sphinx(audio)
        if len(test_text) == 0:
            continue
    except sr.UnknownValueError:
        continue

    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())

    audio = whisperx.load_audio(audio_file)
    result = whisper_model.transcribe(audio, batch_size=batch_size)

    try:
        trans = result["segments"][0]["text"]
        if len(trans) == 0:
            continue
    except IndexError:
        continue

    text = trans
    new_line = {"role": "User", "date": date, "time": time_2, "content": text}

    print("You:" + text)
    with open(r"conversation.jsonl", "a", encoding="UTF-8") as c:
        c.write("\n" + json.dumps(new_line, ensure_ascii=False))

    devices = [os.getenv("DEVICE_1"), os.getenv("DEVICE_2")]

    if tuya == True:
        sentence = "Activate [device]."
        input_sentence = trans.lower()
        for word in devices:
            if word in input_sentence:
                modified_sentence = replace_device(sentence, word)

                input_sentence = keep_sentence_with_word(input_sentence, word)
                input_sentence = input_sentence.translate(
                    str.maketrans("", "", string.punctuation)
                )
                similarity = test_equivalence(modified_sentence, input_sentence)
                if similarity >= 0.5:
                    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
                    openapi.connect()
                    if word == os.getenv("DEVICE_1"):
                        commands = {"commands": [{"code": "switch_1", "value": True}]}
                        openapi.post(os.getenv("DEVICE_1_ID"), commands)
                    if word == os.getenv("DEVICE_2"):
                        commands = {"commands": [{"code": "switch_1", "value": True}]}
                        openapi.post(os.getenv("DEVICE_2_ID"), commands)
                elif similarity < 0.001:
                    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
                    openapi.connect()
                    if word == os.getenv("DEVICE_1"):
                        commands = {"commands": [{"code": "switch_1", "value": False}]}
                        openapi.post(os.getenv("DEVICE_1_ID"), commands)
                    if word == os.getenv("DEVICE_2"):
                        commands = {"commands": [{"code": "switch_1", "value": False}]}
                        openapi.post(os.getenv("DEVICE_2_ID"), commands)
    else:
        pass

    apps = [
        "youtube",
        "brave",
        "discord",
        "spotify",
        "explorer",
        "epic games launcher",
        "tower of fantasy",
        "steam",
        "minecraft",
        "clip studio paint",
        "premiere pro",
        "media encoder",
        "photoshop",
        "audacity",
        "obs",
        "vscode",
        "terminal",
        "synapse",
        "via",
    ]

    sentence = "Activate [app]."
    input_sentence = trans.lower()

    for word in apps:
        if word in input_sentence:
            modified_sentence = replace_app(sentence, word)
            input_sentence = keep_sentence_with_word(input_sentence, word)
            input_sentence = input_sentence.translate(
                str.maketrans("", "", string.punctuation)
            )
            similarity = test_equivalence(modified_sentence, input_sentence)
            if similarity >= 0.5:
                start(word, match_closest=True)
            elif similarity < 0.001:
                end(word, match_closest=True)
    else:
        pass

    query = f"""{text}"""

    results = memory.search(query, top_n=2)

    extracted_dicts = [result["chunk"] for result in results]

    line1 = str(extracted_dicts[0])
    line2 = str(extracted_dicts[1])

    # Read the file and store the lines in the list
    with open("conversation.jsonl", "r", encoding="UTF-8") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    lines = "\n".join(lines)
    lines = lines.splitlines()

    # Check if there are at least 5 lines in the file (6 lines to read and 1 line to exclude)
    if len(lines) >= 5:
        # Extract the last 5 lines (excluding the last line) into a string
        last_six_lines = "\n".join(lines[-5:-1])

        # Iterate over the lines to check
        if line1 not in last_six_lines:
            # If not found in last_six_lines, search for it in the entire file
            found = False
            for i, line in enumerate(lines):
                if line == line1:
                    # If found, append line_to_check and the line directly after/before it to the top of last_six_lines
                    found = True
                    if '''{"role": "User"''' in line:
                        last_six_lines = (
                            line1 + "\n" + str(lines[i + 1]) + "\n" + last_six_lines
                        )
                        break
                    elif '''{"role": "M.I.T.S.U.H.A."''' in line:
                        last_six_lines = (
                            str(lines[i - 1]) + "\n" + line1 + "\n" + last_six_lines
                        )
                        break
            if not found:
                # If still not found, append only line_to_check at the top without the line directly after it
                last_six_lines = line1 + "\n" + last_six_lines
        if line2 not in last_six_lines:
            # If not found in last_six_lines, search for it in the entire file
            found = False
            for i, line in enumerate(lines):
                if line == line2:
                    # If found, append line_to_check and the line directly after/before it to the top of last_six_lines
                    found = True
                    if '''{"role": "User"''' in line:
                        last_six_lines = (
                            line2 + "\n" + str(lines[i + 1]) + "\n" + last_six_lines
                        )
                        break
                    elif '''{"role": "M.I.T.S.U.H.A."''' in line:
                        last_six_lines = (
                            str(lines[i - 1]) + "\n" + line2 + "\n" + last_six_lines
                        )
                        break
            if not found:
                # If still not found, append only line_to_check at the top without the line directly after it
                last_six_lines = line2 + "\n" + last_six_lines
    else:
        last_six_lines = lines

    memory.save(f"""["{new_line}"]""")

    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time_1 = now.strftime("%H:%M:%S")

    prompt = (
        lore
        + "\n\n"
        + str(last_six_lines)
        + str(new_line)
        + f'\n{{"role": "M.I.T.S.U.H.A.", "date": "{date}", "time": "{time_1}", "content": "'
    )
    prompt = str(prompt)

    # generate a response (takes several seconds)
    input_ids = ExLlamatokenizer.encode(str(prompt))
    sys.stdout.flush()

    generator.begin_stream(input_ids, settings)

    generated_tokens = 0

    emotion_hotkey_map = {
        "(wave)": "6",
        "(thumbs-up)": "7",
        "(nodding)": "8",
        "(shaking head)": "9",
        "(clap)": "0",
    }

    print("M.I.T.S.U.H.A.: ", end="")
    generated_text = ""  # Initialize an empty string to store the generated text
    while True:
        chunk, eos, _ = generator.stream()
        generated_tokens += 1
        generated_text += chunk  # Append each chunk to the generated_text variable
        found_emotion = False
        for emotion, hotkey in emotion_hotkey_map.items():
            if chunk == emotion:
                found_emotion = True
                break
        if not found_emotion:
            print(chunk, end="")
        sys.stdout.flush()
        if eos or generated_tokens == max_new_tokens:
            break
    print()
    response = generated_text

    new_line = {
        "role": "M.I.T.S.U.H.A.",
        "date": date,
        "time": time_1,
        "content": response,
    }

    with open(r"conversation.jsonl", "a", encoding="UTF-8") as c:
        c.write("\n" + json.dumps(new_line, ensure_ascii=False))

    memory.save(f"""["{new_line}"]""")

    for emotion, hotkey in emotion_hotkey_map.items():
        if emotion in response.lower():
            response = re.sub(re.escape(emotion), "", response, flags=re.IGNORECASE)
            pyautogui.hotkey("ctrl", "alt", hotkey)
            break

    voice_vits(text=response, lang=lang_code)

    filename = "out.wav"
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype="float32")
    # sd.default.device = "Speakers (Realtek(R) Audio), MME"
    # sd.default.device = "Headphones (AirPods Pro), MME"
    sd.default.device = "CABLE Input (VB-Audio Virtual C, MME"

    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing

    if check_goodbye(trans):
        break
    else:
        continue
