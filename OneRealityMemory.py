import speech_recognition as sr
import os
import sounddevice as sd
import soundfile as sf
import openai
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tuya_connector import TuyaOpenAPI
import string
from AppOpener import open as start, close as end
import json
from hyperdb import HyperDB
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from datetime import datetime
import whisperx
###
# Set to True if you want to use tuya
tuya = True
###

#Load env variables
load_dotenv()

# ExLlamaV2
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exllamav2 import (
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer,
)

from exllamav2.generator import (
    ExLlamaV2StreamingGenerator,
    ExLlamaV2Sampler
)

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
generator.set_stop_conditions(['"}'])

# Settings

settings = ExLlamaV2Sampler.Settings()
settings.temperature = 0.85
settings.top_k = 50
settings.top_p = 0.8
settings.token_repetition_penalty = 1.15
settings.disallow_tokens(ExLlamatokenizer, [ExLlamatokenizer.eos_token_id])

max_new_tokens = 250

# WhisperX
device = "cuda"
devive_index = "1"
audio_file = r"temp.wav"
batch_size = 16 # reduce if low on GPU mem
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)
language = "en"
model = os.getenc("WHISPERX_MODEL")

whisper_model = whisperx.load_model("large-v2", device, language=language, compute_type=compute_type, asr_options={"initial_prompt": "A chat between a user and an artificial intelligence assistant named M.I.T.S.U.H.A."})

# VITS api
abs_path = os.path.dirname(__file__)
base = "http://127.0.0.1:23456"

# Load documents from the JSONL file
documents = []

with open("conversation.jsonl", "r", encoding="utf-8") as f:
    for line in f:
         documents.append(json.loads(line))

# Instantiate HyperDB with the list of documents and the key "description"
model = SentenceTransformer(os.getenv("SENTENCE_TRANSFORMER"))
db = HyperDB(documents, key="info.description",
             embedding_function=model.encode)

# Save the HyperDB instance to a file
db.save("conversation.pickle.gz")

# set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_KEY")

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
model = AutoModelForSequenceClassification.from_pretrained(os.getenv("NLI_RTE_TRANSFORMER"))

# set up Llama model
lore = os.getenv("LORE")

print('''
  _____              ______             _ _           
 / ___ \            (_____ \           | (_)_         
| |   | |____   ____ _____) ) ____ ____| |_| |_ _   _ 
| |   | |  _ \ / _  |_____ ( / _  ) _  | | |  _) | | |
| |___| | | | ( (/ /      | ( (/ ( ( | | | | |_| |_| |
 \_____/|_| |_|\____)     |_|\____)_||_|_|_|\___)__  |
                                               (____/
        Bridging the real and virtual worlds
              [PROJECT M.I.T.S.U.H.A.]
''')

# tts function
def voice_vits(text, id=0, format="wav", lang="auto", length=1, noise=0.667, noisew=0.8, max=50):
    fields = {
        "text": text,
        "id": str(id),
        "format": format,
        "lang": lang,
        "length": str(length),
        "noise": str(noise),
        "noisew": str(noisew),
        "max": str(max)
    }
    boundary = '----VoiceConversionFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))

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
    batch = tokenizer(text1, text2, return_tensors='pt').to(model.device)
    with torch.no_grad():
        proba = torch.softmax(model(**batch).logits, -1)
    return proba.cpu().numpy()[0, model.config.label2id['ENTAILMENT']]

def test_equivalence(text1, text2):
    return test_entailment(text1, text2) * test_entailment(text2, text1)

def replace_device(sentence, word):
    return sentence.replace("[device]", word)

def replace_app(sentence, word):
    return sentence.replace("[app]", word)

def keep_sentence_with_word(text, word):
    sentences = text.split('.')
    filtered_sentences = [sentence.strip() + '.' for sentence in sentences if word in sentence]
    result = ' '.join(filtered_sentences)
    return result

def keep_sentence_with_word(text, word):
    sentences = re.split(r'[.,!?]', text)
    filtered_sentences = [sentence.strip() + punct for sentence, punct in zip(sentences, re.findall(r'[.,!?]', text)) if word in sentence]
    result = ' '.join(filtered_sentences)
    return result

while True:
    print("Speak now!")
    
    with mic as source:
        audio = r.listen(source, timeout = None)
        
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M:%S")
    
    test_text = r.recognize_sphinx(audio)
    if len(test_text) == 0:
        continue
    else:
        pass
    
    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())

    audio = whisperx.load_audio(audio_file)
    result = whisper_model.transcribe(audio, batch_size=batch_size)
    trans = result["segments"][0]["text"]

    if len(trans) == 0:
        continue
    else:
        pass
    
    text = trans
    new_line = {"role": "User", "date": date, "time": time, "content": text}
    
    print("You:" + text)
    with open(r"conversation.jsonl", "a", encoding='UTF-8') as c:
        c.write("\n" + json.dumps(new_line, ensure_ascii=False))
        
    documents.append(new_line)
    db.save("conversation.pickle.gz")

    devices = [
        os.getenv("DEVICE_1"),
        os.getenv("DEVICE_2")
    ]
    if tuya == True:
        sentence = "Activate [device]."
        input_sentence = trans.lower()
        for word in devices:
            if word in input_sentence:
                modified_sentence = replace_device(sentence, word)

                input_sentence = keep_sentence_with_word(input_sentence, word)
                input_sentence = input_sentence.translate(str.maketrans('', '', string.punctuation))
                similarity = (test_equivalence(modified_sentence, input_sentence))
                if similarity >= 0.5:
                    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
                    openapi.connect()
                    if word == os.getenv("DEVICE_1"):
                        commands = {'commands': [{'code':'switch_1','value': True}]}	
                        openapi.post(os.getenv("DEVICE_1_ID"), commands)
                    if word == os.getenv("DEVICE_2"):
                        commands = {'commands': [{'code':'switch_1','value': True}]}	
                        openapi.post(os.getenv("DEVICE_2_ID"), commands)
                elif similarity < 0.001:
                    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
                    openapi.connect()
                    if word == os.getenv("DEVICE_1"):
                        commands = {'commands': [{'code':'switch_1','value': False}]}	
                        openapi.post(os.getenv("DEVICE_1_ID"), commands)
                    if word == os.getenv("DEVICE_2"):
                        commands = {'commands': [{'code':'switch_1','value': False}]}	
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
    "via"
    ]
    
    sentence = "Activate [app]."
    input_sentence = trans.lower()
    
    for word in apps:
        if word in input_sentence:
            modified_sentence = replace_app(sentence, word)
            print(modified_sentence)
            input_sentence = keep_sentence_with_word(input_sentence, word)
            input_sentence = input_sentence.translate(str.maketrans('', '', string.punctuation))
            print(input_sentence)
            similarity = (test_equivalence(modified_sentence, input_sentence))
            print(similarity)
            if similarity >= 0.5:
                start(word, match_closest=True)
            elif similarity < 0.001:
                end(word, match_closest=True)
    else:
        pass
    
    db.load("conversation.pickle.gz")
    
    results = db.query(new_line, top_k=2)

    extracted_dicts = [item for item, _ in results]

    line1 = str(extracted_dicts[0])
    line2 = str(extracted_dicts[1])
    
    # Specify the file name
    file_name = "conversation.jsonl"

    # Initialize an empty list to store the lines
    lines = []

    # Read the file and store the lines in the list
    with open(file_name, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    # Check if there are at least 7 lines in the file (6 lines to read and 1 line to exclude)
    if len(lines) >= 5:
        # Extract the last 6 lines (excluding the last line) into a string
        last_six_lines = ''.join(lines[-5:-1])

        # Define a list of lines to check
        lines_to_check = str(extracted_dicts)

        # Iterate over the lines to check
        for line_to_check in lines_to_check:
            if line_to_check not in last_six_lines:
                # If not found in last_six_lines, search for it in the entire file
                found = False
                for i, line in enumerate(lines):
                    if line == line_to_check:
                        # If found, append line_to_check and the line directly after it to the top of last_six_lines
                        last_six_lines = line_to_check + lines[i + 1] + last_six_lines
                        found = True
                        break
                
                if not found:
                    # If still not found, append only line_to_check at the top without the line directly after it
                    last_six_lines = line_to_check + last_six_lines
    else:
        last_six_lines = lines
            
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M:%S")

    prompt = lore + "\n" + "\n" + str(last_six_lines) + str(new_line) + f'\n{{"role": "M.I.T.S.U.H.A.", "date": "{date}", "time": "{time}", "content": "'
    prompt = str(prompt)
    
    # generate a response (takes several seconds)
    input_ids = ExLlamatokenizer.encode(str(prompt))
    sys.stdout.flush()
    
    generator.begin_stream(input_ids, settings)
    
    generated_tokens = 0

    print("M.I.T.S.U.H.A.: ", end = "")
    generated_text = ""  # Initialize an empty string to store the generated text
    while True:
        chunk, eos, _ = generator.stream()
        generated_tokens += 1
        generated_text += chunk  # Append each chunk to the generated_text variable
        print (chunk, end = "")
        sys.stdout.flush()
        if eos or generated_tokens == max_new_tokens: break
    print()
    response = generated_text

    new_line = {"role": "M.I.T.S.U.H.A.", "date": date, "time": time, "content": response}
    
    with open(r"conversation.jsonl", "a", encoding='UTF-8') as c:
        c.write("\n" + json.dumps(new_line, ensure_ascii=False))
        
    documents.append(new_line)
    db.save("conversation.pickle.gz")
    
    voice_vits(text=response, lang="en")
    
    filename = 'out.wav'
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='float32')
    #sd.default.device = "Speakers (Realtek(R) Audio), MME"
    #sd.default.device = "Headphones (AirPods Pro), MME"
    sd.default.device = "CABLE Input (VB-Audio Virtual C, MME"
    
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing

    if check_goodbye(trans):
        break
    else:
        continue