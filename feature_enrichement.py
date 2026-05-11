# Read and write
import csv 

with open("group_transcript.csv", 'r', encoding='utf-8') as infile, \
     open("group_transcript_enriched.csv", 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + ['has_question_mark', 'num_words_in_text', 'text_size_chars', 'speech_rate_wps'])

    
    writer.writeheader()
    for row in reader:
        row['has_question_mark'] = '?' in row.get('text', '')
        row['num_words_in_text'] = len(row.get('text', '').split())
        row['text_size_chars'] = len(row.get('text', ''))
        row['speech_rate_wps'] = int(row['num_words_in_text'] // float(row['time_taken_sec']))
        writer.writerow(row)

    

