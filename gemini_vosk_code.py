import os
import csv
from google import genai
import queue
import json
import sounddevice as sd
from datetime import datetime
from vosk import Model, KaldiRecognizer
import time
import wave

#Configuring Models
GEMINI_MODEL = "gemini-2.5-flash"
VOSK_MODEL = "vosk-model-en-us-0.22-lgraph"
SAMPLE_RATE = 16000
OUTPUT_CSV = "group_transcript.csv"

#gemini transcript clean
def corrected_text(raw_text):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = f"Correct this transcript and return only the corrected sentence: {raw_text}"
    response = client.models.generate_content(model = GEMINI_MODEL, contents = prompt)
    return response.text.strip()


#def record_turn(): #maybe needed
q = queue.Queue()

def callback(indata,frames,time,status): #start recording and transcribing
    if status:
        print(status)
    q.put(bytes(indata))
    
    model = Model(VOSK_MODEL)
    recognizer = KaldiRecognizer(model,SAMPLE_RATE)
    start_time =time.time()
   
    print("Recording ... Press ENTER to finish.")

    full_text = ""

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text","")
                if text:
                    print("You said:", text)
                    full_text += text + " "
    
    final_result = json.loads(recognizer.FinalResult())
    final_text += final_result.get("text","")

    duration = round(time.time()-start_time, 1)
    return full_text.strip(), duration
    


#def transcribe_file(): #may be needed as i think vosk is more an real time audio input



#def main(): 
    #for the transcription we may need an option for both microphone and file input