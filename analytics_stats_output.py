import csv


def analyze_meeting_data(file_path):
    # Open the CSV file
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Create empty dictionaries to store data
        word_count = {}
        question_count = {}
        speaking_time = {}
        
        # Loop through each row in the CSV
        for row in reader:
            
            # Add words for this speaker
            if row['name'] in word_count:
                word_count[row['name']] += int(row['num_words_in_text'])
            else:
                word_count[row['name']] = int(row['num_words_in_text'])
            
            # Add question for this speaker
            if row['has_question_mark'].upper() == 'TRUE':
                if row['name'] in question_count:
                    question_count[row['name']] += 1
                else:
                    question_count[row['name']] = 1
            
            # Add speaking time for this speaker
            if row['name'] in speaking_time:
                speaking_time[row['name']] += float(row['time_taken_sec'])
            else:
                speaking_time[row['name']] = float(row['time_taken_sec'])
    
    # Find who spoke the most words
    most_words_speaker = ""
    most_words_count = 0
    for speaker in word_count:
        if word_count[speaker] > most_words_count:
            most_words_count = word_count[speaker]
            most_words_speaker = speaker
    
    
    # Find who asked the most questions
    most_questions_speaker = ""
    most_questions_count = 0
    for speaker in question_count:
        if question_count[speaker] > most_questions_count:
            most_questions_count = question_count[speaker]
            most_questions_speaker = speaker
    
    
    # Calculate total speaking time
    total_time = 0
    for speaker in speaking_time:
        total_time += speaking_time[speaker]
    
    # Calculate average speaking time
    num_speakers = len(speaking_time)
    average_time = total_time / num_speakers
    
    
    # Print results
    print("=" * 50)
    print("Meeting Analytics Report")
    print("=" * 50)
    print()
    
    print("Most words:", most_words_speaker, "-", most_words_count, "words")
    print("Total speaking time:", total_time, "seconds")
    print("Average speaking time per speaker:", round(average_time,2), "seconds")
    print("Most questions:", most_questions_speaker, "-", most_questions_count, "questions")
    print()
    

def main():
    file_path = "group_transcript_enriched.csv"
    analyze_meeting_data(file_path)


if __name__ == "__main__":
    main()