import os
import csv
from google import genai
import queue
import json
import sounddevice as sd
from datetime import datetime
from vosk import Model, KaldiRecognizer
import time

