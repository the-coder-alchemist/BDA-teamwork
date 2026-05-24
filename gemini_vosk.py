"""
Meeting Pipeline: Vosk Recording + Gemini Cleanup
==================================================

Captures live audio from the default microphone, transcribes it on-the-fly
with the offline Vosk speech-recognition engine, and stores each recording
as a row in a CSV. Once the user quits the record loop, every raw transcript
is sent to Google's Gemini model in a single batched call to be cleaned up
(spelling, punctuation, casing) before the final CSV is written out.

The CSV columns produced are:
    timestamp, name, raw_text_vosk, text, time_taken_sec

Where ``raw_text_vosk`` is what Vosk heard and ``text`` is the Gemini-corrected
version.

Requirements:
    * ``GEMINI_API_KEY`` set as an environment variable
    * A working microphone available to ``sounddevice``
    * The Vosk model directory ``vosk-model-en-us-0.22-lgraph`` present in
      the working directory

Usage:
    python gemini_vosk.py

    At the prompt, choose ``R`` to record a new utterance (and provide the
    speaker's name when asked) or ``Q`` to finish and trigger cleanup.
"""

# Metadata
__author__ = []
__credits__ = ["Carys Williams","Gary Murphy", "William McKenna", "Mei Len Vorkel", "Samuel Weldemariam", "Toby Lock"]
__version__ = "1.0.0"

# Custom Academic Attribution Matrix
__team__ = "The Pipeline"
__module__ = "Big Data Analytics (BUCI065H7)"
__assignment__ = "Assignment 1 - Startup Meeting Speech Analytics"

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
    """
    Send a list of raw transcripts to Gemini for grammar/spelling correction.

    All transcripts are bundled into a single numbered prompt so the entire
    batch can be cleaned in one API call (much cheaper and faster than one
    call per row). Gemini is instructed to return the same numbered list with
    each line corrected, preserving the original ordering.

    Args:
        texts (list[str]): The raw Vosk transcripts, in the order they were
            recorded.

    Returns:
        str: Gemini's raw response. The caller is responsible for splitting
        the numbered lines back out (see ``main`` for how this is done).

    Side effects:
        Reads ``GEMINI_API_KEY`` from the environment to authenticate with
        the Gemini API.

    Example:
        >>> correct_all_text(["the rats everyone", "i've been tracking use a"])
        '1. Hi everyone.\\n2. I\\'ve been tracking users.'
    """

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
    prompt = f"Correct each transcript and return only the corrected sentences, numbered the same way:\n{numbered}"
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text.strip()

#Recording transcript
def realtime_transcription():
    """
    Record audio from the microphone and stream it through Vosk until Ctrl+C.

    Opens a raw input audio stream at 16 kHz mono and feeds each audio block
    into a Vosk recogniser as it arrives. Partial recognition results are
    accumulated into a list, and the final pending result is flushed when
    the user interrupts with Ctrl+C. The accumulated text fragments are
    joined at the end with single spaces.

    Returns:
        tuple[str, float]: The full transcribed text (joined with spaces and
        stripped of leading/trailing whitespace) and the recording duration
        in seconds, rounded to 2 decimals.

    Side effects:
        Reads from the default microphone via ``sounddevice``. Prints status
        messages and a "Recording stopped" notice on Ctrl+C.

    Example:
        >>> text, secs = realtime_transcription()
        Recording ... Press Ctrl+C to finish.
        ^C
        Recording stopped
        >>> text
        'hello everyone thanks for joining'
    """

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
    """
    Append one transcript row to the output CSV, writing a header if needed.

    Checks whether the file already exists; if not, writes the header row
    first. Then appends the supplied dictionary as a single CSV row.

    Args:
        data (dict): Must contain the keys ``timestamp``, ``name``,
            ``raw_text_vosk``, ``text`` and ``time_taken_sec``.

    Returns:
        None. The row is persisted to ``OUTPUT_CSV``.

    Example:
        >>> save_to_csv({
        ...     "timestamp": "2026-05-10T12:58:58",
        ...     "name": "Toby Lock",
        ...     "raw_text_vosk": "hello everyone",
        ...     "text": "",
        ...     "time_taken_sec": 9.33,
        ... })
    """

    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=["timestamp","name","raw_text_vosk","text","time_taken_sec"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def main():
    """
    Run the interactive record/quit loop, then batch-correct the transcripts.

    Prompts the user repeatedly for a mode:
        * ``R`` - ask for the speaker's name, record an utterance, save it
        * ``Q`` - exit the loop and proceed to cleanup

    Once the loop exits, the function reads the saved CSV with pandas, sends
    every ``raw_text_vosk`` value to Gemini in a single batch via
    ``correct_all_text``, parses the numbered response back into a list, and
    overwrites the CSV with the corrected ``text`` column populated.

    Returns:
        None. All output is written to ``OUTPUT_CSV``.

    Example:
        >>> main()
        Meeting Pipeline
        Choose mode: [R]ecord or [Q]uit: r
        Who is speaking? Toby Lock
        Recording ... Press Ctrl+C to finish.
        ...
    """

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