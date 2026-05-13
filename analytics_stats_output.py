import csv


def analyze_meeting_data(file_path):
    # Open the CSV file
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Create empty dictionaries to store data
        word_count = {}
        speaking_time = {}
        
        # Loop through each row in the CSV
        for row in reader:
            speaker = row['name']
            words = int(row['num_words_in_text'])
            time_taken = float(row['time_taken_sec'])
            
            # Add words for this speaker
            if speaker in word_count:
                word_count[speaker] += words
            else:
                word_count[speaker] = words
            
            
            # Add speaking time for this speaker
            if speaker in speaking_time:
                speaking_time[speaker] += time_taken
            else:
                speaking_time[speaker] = time_taken
    
    
    
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
    
    print("Total speaking time:", total_time, "seconds")
    print("Average speaking time per speaker:", round(average_time,2), "seconds")
    print()
    print("=" * 50)


def main():
    file_path = "group_transcript_enriched.csv"
    analyze_meeting_data(file_path)


if __name__ == "__main__":
    main()