# Read and write
import csv 

with open("group_transcript.csv", 'r', encoding='utf-8') as infile, \
     open("group_transcript_enriched.csv", 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + ['has_question_mark', 'num_words_in_text',])

    
    writer.writeheader()
    for row in reader:
        row['has_question_mark'] = '?' in row.get('text', '')
        row['num_words_in_text'] = len(row.get('text', '').split())
        writer.writerow(row)

    

