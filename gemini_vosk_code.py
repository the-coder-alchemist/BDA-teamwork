'''
def transcribe_file(file_path):
    wf = wave.open(file_path, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)
    
    final_result = json.loads(recognizer.FinalResult())
    duration = round(wf.getnframes() / wf.getframerate(), 2)
    return final_result.get("text", ""), duration


elif mode == 'f':
    path = input("Enter file path to .wav file:")
    raw_text,duration = transcribe_file(path)
'''