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
import pandas as pd

#Configuring Models
GEMINI_MODEL = "gemini-2.5-flash-lite"
VOSK_MODEL = "vosk-model-en-us-0.22-lgraph"
SAMPLE_RATE = 16000
OUTPUT_CSV = "test_transcript.csv"

model = Model(VOSK_MODEL)

#gemini transcript clean
def correct_all_text(texts):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
    prompt = f"Correct each transcript and return only the corrected sentences, numbered the same way:\n{numbered}"
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text.strip()

#Recording transcript
def realtime_transcription():
    q = queue.Queue()
    def callback(indata, frames, time_info, status): #start recording and transcribing
        if status:
            print(status)
        q.put(bytes(indata))
    
    recognizer = KaldiRecognizer(model,SAMPLE_RATE)
    start_time =time.time()
    full_text = ""
   
    print("Recording ... Press Ctrl+C to finish.")

    try:
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
                        full_text += text + " "
    
    except KeyboardInterrupt:
        print("\nRecording stopped")
    
    final_result = json.loads(recognizer.FinalResult())
    final_text = final_result.get("text", "")
    if final_text:
        full_text += final_text

    duration = round(time.time()-start_time, 2)
    return full_text.strip(), duration

#Write to csv
def save_to_csv(data):
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=["timestamp","name","raw_text_vosk","text","time_taken_sec"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def main():
    print("Meeting Pipeline")

    while True:
        mode = input("Choose mode: [R]ecord or [Q]uit:").lower()
        if mode == 'q':
            break
        elif mode == 'r':
            speaker = input("Who is speaking? ")
            raw_text, duration = realtime_transcription()
            save_to_csv({
            "timestamp": datetime.now().isoformat(),
            "raw_text_vosk": raw_text,
            "text": "",
            "time_taken_sec": duration,
            "name":speaker
            })
            print("Transcription complete")
        else:
            print("Invalid entry, Please enter R or Q")
            continue

    transcript = pd.read_csv(OUTPUT_CSV)
    transcript["text"] = transcript["text"].astype(object)

    print("Correcting transcriptions...")
    corrected = correct_all_text(transcript["raw_text_vosk"].tolist())

    # parse numbered response back into rows
    lines = [line.split(". ", 1)[1] for line in corrected.split("\n") if line.strip()]
    transcript["text"] = lines

    transcript.to_csv(OUTPUT_CSV, index=False)
    print("All transcriptions corrected")
if __name__ == "__main__":
    main()