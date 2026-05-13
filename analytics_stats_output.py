import csv


def analyze_meeting_data(file_path):
    # Open the CSV file
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Variable to store total speaking time
        total_time = 0
        
        # Loop through each row in the CSV
        for row in reader:
            time_taken = float(row['time_taken_sec'])
            
            # Add time to total
            total_time = total_time + time_taken
    
    # Print results
    print("=" * 50)
    print("Meeting Analytics Report")
    print("=" * 50)
    print()
    
    print("Total speaking time:", total_time, "seconds")
    
    print("=" * 50)


def main():
    file_path = "group_transcript_enriched.csv"
    analyze_meeting_data(file_path)


if __name__ == "__main__":
    main()