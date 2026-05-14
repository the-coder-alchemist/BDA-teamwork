import csv


def analyze_meeting_data(file_path):
    # Open the CSV file
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Create empty dictionaries to store data
        word_count = {}
        question_count = {}
        speaking_time = {}
        speech_rate_total = {}
        speech_rate_count = {}

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
                speaking_time[row['name']] += round(float(row['time_taken_sec']), 2)
            else:
                speaking_time[row['name']] = round(float(row['time_taken_sec']), 2)

            # Add speech rate to list for this speaker
            if row['name'] in speech_rate_total:
                speech_rate_total[row['name']] += float(row['speech_rate_wps'])
                speech_rate_count[row['name']] += 1
            else:
                speech_rate_total[row['name']] = float(row['speech_rate_wps'])
                speech_rate_count[row['name']] = 1


    # Find who spoke the most words
    most_words_speaker = ""
    most_words_count = 0
    for speaker in word_count:
        if word_count[speaker] > most_words_count:
            most_words_count = word_count[speaker]
            most_words_speaker = speaker

    # Find who spoke the least words
    least_words_count = min(word_count.values())
    least_words_speaker = min(word_count, key=word_count.get)
    
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

    # Calculate top 5 speakers by total time - using Bubble sort 
    speaking_time_list = list(speaking_time.items()) #make the dict into a list of tuples for sorting
    n = len(speaking_time_list)
    for i in range(n):
        for j in range(0,n-i-1):
            if speaking_time_list[j][1] < speaking_time_list[j+1][1]: #compare the second element of the tuple (the time)
                speaking_time_list[j], speaking_time_list[j+1] = speaking_time_list[j+1], speaking_time_list[j] #swap the tuples
    sorted_speaking_time5 = speaking_time_list[:5]

    
    # Calculate average speaking time
    num_speakers = len(speaking_time)
    average_time = total_time / num_speakers
    
    
    # Print results
    print("=" * 50)
    print("Meeting Analytics Report")
    print("=" * 50)
    print()
    
    print("Most words:", most_words_speaker, "-", most_words_count, "words")
    print("Least words:", least_words_speaker, "-", least_words_count, "words")
    print("Total speaking time:", total_time, "seconds")
    print("Average speaking time per speaker:", round(average_time,2), "seconds")
    print("Most questions:", most_questions_speaker, "-", most_questions_count, "questions")
    print()
    print("Top 5 speakers by total time:")
    for speaker, time in sorted_speaking_time5:
        print(f"{speaker}: {time:.2f} seconds")
    print()

      # Calculate and print average speech rate for each speaker
    for speaker in speech_rate_total:
        average = speech_rate_total[speaker] / speech_rate_count[speaker]
        print(speaker, "average speech rate:", round(average, 2), "words/second")
    print()
    print("=" * 50)

def main():
    file_path = "group_transcript_enriched.csv"
    analyze_meeting_data(file_path)


if __name__ == "__main__":
    main()