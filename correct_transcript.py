import os
from google import genai
import pandas as pd

GEMINI_MODEL = "gemini-2.5-flash-lite"
OUTPUT_CSV = "group_transcript.csv"

def correct_all_text(texts):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
    prompt = f"Correct each transcript and return only the corrected sentences, numbered the same way:\n{numbered}"
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text.strip()

transcript = pd.read_csv(OUTPUT_CSV)
transcript["text"] = transcript["text"].astype(object)

print("Correcting transcriptions...")
corrected = correct_all_text(transcript["raw_text_vosk"].tolist())

lines = [line.split(". ", 1)[1] for line in corrected.split("\n") if line.strip()]

if len(lines) == len(transcript):
    transcript["text"] = lines
    transcript.to_csv(OUTPUT_CSV, index=False)
    print("All transcriptions corrected")
else:
    print(f"Warning: expected {len(transcript)} lines but got {len(lines)}")
    print(corrected)