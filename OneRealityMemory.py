import speech_recognition as sr
import os
import winsound
import openai
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tuya_connector import TuyaOpenAPI
import string
from AppOpener import open as start, close as end
from llama_cpp import Llama
import json
from hyperdb import HyperDB
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
###
# Set to True if you want to use tuya
tuya = True
###

# VITS api
abs_path = os.path.dirname(__file__)
base = "http://127.0.0.1:23456"

#Load env variables
load_dotenv()

# Load documents from the JSONL file
documents = []

with open("conversation.jsonl", "r") as f:
    for line in f:
        documents.append(json.loads(line))

# Instantiate HyperDB with the list of documents and the key "description"
model = SentenceTransformer(os.getenv("SENTENCE_TRANSFORMER"))
db = HyperDB(documents, key="info.description",
             embedding_function=model.encode)

# Save the HyperDB instance to a file
db.save("conversation.pickle.gz")

# set up Llama
LLM = Llama(model_path=os.getenv("LLM"), n_ctx=2048, n_gpu_layers=-1, verbose=False)

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
with open(r"conversation.txt", "r") as c:
        conversation = c.read

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

    test_text = r.recognize_sphinx(audio)
    if len(test_text) == 0:
        continue
    else:
        pass

    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())
        
    if os.getenv("LANGUAGE") == "English":
        LANGUAGE = "en"
    elif os.getenv("LANGUAGE") == "한국어":
        LANGUAGE = "ko"
    elif os.getenv("LANGUAGE") == "日本語":
        LANGUAGE = "ja"
    elif os.getenv("LANGUAGE") == "简体中文":
        LANGUAGE = "zh"

    audio_file= open("temp.wav", "rb")
    trans = openai.Audio.transcribe(
        model=os.getenv("WHISPER_MODEL"),
        file=audio_file,
        temperature=0.1,
        language=LANGUAGE
    )

    if len(trans['text']) == 0:
        continue
    else:
        pass
    
    text = trans['text']
    new_line = {"role": "User", "content": text}
    
    print("You:" + trans['text'])
    with open(r"conversation.jsonl", "a") as c:
        c.write("\n" + json.dumps(new_line))
        
    documents.append(new_line)
    db.save("conversation.pickle.gz")

    devices = [
        "gaming mode",
        "night light",
        "nightlight"
    ]

    sentence = "Activate [device]."
    input_sentence = trans['text'].lower()
    if tuya == True:
        for word in devices:
            if word in input_sentence:
                modified_sentence = replace_device(sentence, word)

                input_sentence = keep_sentence_with_word(input_sentence, word)
                input_sentence = input_sentence.translate(str.maketrans('', '', string.punctuation))
                print(input_sentence)
                similarity = (test_equivalence(modified_sentence, input_sentence))
                print(similarity)
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
    input_sentence = trans['text'].lower()
    
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

    extracted_dicts_str = "\n".join(str(d) for d in extracted_dicts)

    with open("conversation.jsonl", "r") as f:
        lines = f.readlines()

    # Overwrite the 'documents' list with the desired user-megumin pairs
    documents = []
    i = 0
    while i < len(lines):
        line_data = json.loads(lines[i].strip())
        if line_data in extracted_dicts:
            megumin_line = json.loads(lines[i + 1].strip())  # Assuming the next line is always Megumin's response
            documents.append(line_data)
            documents.append(megumin_line)
            i += 2  # Skip the next line as it's already included
        else:
            i += 1

    prompt = lore + "\n" + "\n".join(str(json.dumps(doc, indent=None)) for doc in documents) + "\n" + str(new_line) + "\n{'role': 'Megumin', 'content': "
    
    # generate a response (takes several seconds)
    response = LLM(prompt, echo=False, stream=False, stop=["{"])
    
    # display the response
    response = response["choices"][0]["text"]
    response = response.encode("ascii", "ignore")
    response = response.decode()
    response = response.strip(" '}")
    print("Megumin: " + response)

    new_line = {"role": "Megumin", "content": response}
    
    with open(r"conversation.jsonl", "a") as c:
        c.write("\n" + json.dumps(new_line))
        
    documents.append(new_line)
    db.save("conversation.pickle.gz")

    response = response.replace("\n", " ")
    response = response.replace('"', '\\"')
    voice_vits(text=response, lang=LANGUAGE)
    
    winsound.PlaySound(r"out.wav", winsound.SND_FILENAME)

    if check_goodbye(trans['text']):
        break
    else:
        continue