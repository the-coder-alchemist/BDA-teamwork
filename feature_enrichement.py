"""
Transcript Feature Enrichment
==============================

Reads the raw meeting transcript produced by ``gemini_vosk.py`` and writes 
out an enriched copy with five additional columns derived from the cleaned
``text`` field:

    * ``has_question_mark`` - True if the text contains a "?" character
    * ``num_words_in_text``  - whitespace-split word count
    * ``text_size_chars``    - character length of the text
    * ``speech_rate_wps``    - words per second, rounded to 2 decimals
    * ``speaker_counter``    - the Nth utterance by this speaker (1-indexed)

The script streams the file row-by-row, so memory use stays flat regardless
of transcript length.

Usage:
    Place ``group_transcript.csv`` in the working directory and run::

        python feature_enrichement.py

    The enriched output is written to ``group_transcript_enriched.csv``.
"""

# Metadata
__author__ = []
__credits__ = ["Carys Williams","Gary Murphy", "William McKenna", "Mei Len Vorkel", "Samuel Weldemariam", "Toby Lock"]
__version__ = "1.0.0"

# Custom Academic Attribution Matrix
__team__ = "The Pipeline"
__module__ = "Big Data Analytics (BUCI065H7)"
__assignment__ = "Assignment 1 - Startup Meeting Speech Analytics"

# Read and write
import csv 

with open("group_transcript.csv", 'r', encoding='utf-8') as infile, \
     open("group_transcript_enriched.csv", 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + ['has_question_mark', 'num_words_in_text', 'text_size_chars', 'speech_rate_wps', 'speaker_counter'])

    counter = {}
    speaker_counter = None

    writer.writeheader()
    for row in reader:
        row['has_question_mark'] = '?' in row.get('text', '')
        row['num_words_in_text'] = len(row.get('text', '').split())
        row['text_size_chars'] = len(row.get('text', ''))
        row['speech_rate_wps'] = round(float(row['num_words_in_text'] / float(row['time_taken_sec'])) ,2)
        speaker = row['name']
        counter[speaker] = counter.get(speaker, 0) + 1
        speaker_counter = counter[speaker]
        row['speaker_counter'] = speaker_counter
        writer.writerow(row)

    

