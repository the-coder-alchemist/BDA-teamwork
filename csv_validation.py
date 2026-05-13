import csv
from datetime import datetime


def validate_timestamp(value, field_name, row_num):
    #Check if timestamp is a valid datetime format.
    try:
        datetime.fromisoformat(value)
        return True, None
    except (ValueError, AttributeError):
        return False, f"Row {row_num}: {field_name} '{value}' is not a valid datetime"


def validate_numeric_positive(value, field_name, row_num):
    #Check if value is numeric and greater than 0.
    try:
        num = float(value)
        if num > 0:
            return True, None
        else:
            return False, f"Row {row_num}: {field_name} '{value}' is not greater than 0"
    except (ValueError, TypeError):
        return False, f"Row {row_num}: {field_name} '{value}' is not numeric"


def validate_boolean(value, field_name, row_num):
    #Check if value is a boolean (TRUE/FALSE, True/False, true/false).
    if isinstance(value, bool):
        return True, None
    if isinstance(value, str):
        if value.upper() in ['TRUE', 'FALSE']:
            return True, None
    return False, f"Row {row_num}: {field_name} '{value}' is not a boolean value"


def validate_csv_file(file_path):
    
    validation_errors = []
    row_number = 0
    
 
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
            
            # Validate each row
        for row in reader:
            row_number += 1
            current_row = row_number + 1
                
                # Validate timestamp
            value = row['timestamp']
            is_valid, error_msg = validate_timestamp(value, 'timestamp', current_row)
            if not is_valid:
                validation_errors.append(error_msg)
                
                # Validate time_taken_sec
            value = row['time_taken_sec']
            is_valid, error_msg = validate_numeric_positive(value, 'time_taken_sec', current_row)
            if not is_valid:
                validation_errors.append(error_msg)
                
                # Validate num_words_in_text
            value =row['num_words_in_text']
            is_valid, error_msg = validate_numeric_positive(value, 'num_words_in_text', current_row)
            if not is_valid:
                validation_errors.append(error_msg)
                
                # Validate speech_rate_wps
            value = row['speech_rate_wps']
            is_valid, error_msg = validate_numeric_positive(value, 'speech_rate_wps', current_row)
            if not is_valid:
                validation_errors.append(error_msg)
                
                # Validate has_question_mark
            value = row['has_question_mark']
            is_valid, error_msg = validate_boolean(value, 'has_question_mark', current_row)
            if not is_valid:
                validation_errors.append(error_msg)
                
                # Validate speaker_counter
            value = row['speaker_counter']
            is_valid, error_msg = validate_numeric_positive(value, 'speaker_counter', current_row)
            if not is_valid:
                validation_errors.append(error_msg)
            
            # Print validation results
        if validation_errors:
            print("Validation failed:")
            for error in validation_errors:
                print(f"- {error}")
            return False
        else:
            print("Validation passed!")
            print(f"All {row_number} rows are valid.")
            print("\nSummary:")
            print(f"- Total rows checked: {row_number}")
            print(f"- All timestamps are valid")
            print(f"- All numeric fields are positive numbers")
            print(f"- All boolean fields are valid")
            print(f"- No missing required values")
            return True
                


def main():
    #Main function to run CSV validation.
    file_path = "group_transcript_enriched.csv"
    
    print("=" * 50)
    print("CSV Validation Report")
    print("=" * 50)
    print(f"File: {file_path}\n")
    
    validate_csv_file(file_path)


if __name__ == "__main__":
    main()