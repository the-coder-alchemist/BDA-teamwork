"""
Enriched Transcript CSV Validator
==================================

Validates that an enriched meeting-transcript CSV is well-formed before any
downstream analytics consumes it. Each row is checked for:

    * a parseable ISO 8601 ``timestamp``
    * positive numeric values in ``time_taken_sec``, ``num_words_in_text``,
      ``speech_rate_wps`` and ``speaker_counter``
    * a boolean-compatible value in ``has_question_mark``

The script prints either a "Validation passed!" summary or a list of every
problem it found, annotated with the line number in the source file.

Usage:
    Place an enriched transcript named ``group_transcript_enriched.csv`` in
    the working directory and run::

        python csv_validation.py
"""

# Metadata
__author__ = []
__credits__ = ["Carys Williams","Gary Murphy", "William McKenna", "Mei Len Vorkel", "Samuel Weldemariam", "Toby Lock"]
__version__ = "1.0.0"

# Custom Academic Attribution Matrix
__team__ = "The Pipeline"
__module__ = "Big Data Analytics (BUCI065H7)"
__assignment__ = "Assignment 1 - Startup Meeting Speech Analytics"

import csv
from datetime import datetime


def validate_timestamp(value, field_name, row_num):
    """
    Check whether ``value`` is a valid ISO 8601 datetime string.

    Args:
        value (str): The string to validate (e.g. ``"2026-05-10T12:58:58"``).
        field_name (str): Name of the field being validated. Used to build a
            helpful error message.
        row_num (int): The 1-based line number in the source file. Used in
            the error message so the user can locate the bad row.

    Returns:
        tuple[bool, str | None]: ``(True, None)`` if the value parses,
        otherwise ``(False, "<error message>")``.

    Example:
        >>> validate_timestamp("2026-05-10T12:58:58", "timestamp", 2)
        (True, None)
        >>> validate_timestamp("not a date", "timestamp", 3)
        (False, "Row 3: timestamp 'not a date' is not a valid datetime")
    """

    #Check if timestamp is a valid datetime format.
    try:
        datetime.fromisoformat(value)
        return True, None
    except:
        return False, f"Row {row_num}: {field_name} '{value}' is not a valid datetime"


def validate_numeric_positive(value, field_name, row_num):
    """
    Check whether ``value`` is numeric and strictly greater than zero.

    Args:
        value (str): The string to validate (e.g. ``"9.33"``).
        field_name (str): Name of the field being validated.
        row_num (int): The 1-based line number in the source file.

    Returns:
        tuple[bool, str | None]: ``(True, None)`` if the value is numeric and
        positive, otherwise ``(False, "<error message>")``. Zero and negative
        numbers both fail validation.

    Example:
        >>> validate_numeric_positive("9.33", "time_taken_sec", 2)
        (True, None)
        >>> validate_numeric_positive("0", "time_taken_sec", 3)
        (False, "Row 3: time_taken_sec '0' is not greater than 0")
    """

    #Check if value is numeric and greater than 0.
    try:
        num = float(value)
        if num > 0:
            return True, None
        else:
            return False, f"Row {row_num}: {field_name} '{value}' is not greater than 0"
    except:
        return False, f"Row {row_num}: {field_name} '{value}' is not numeric"


def validate_boolean(value, field_name, row_num):
    """
    Check whether ``value`` represents a boolean.

    Accepts native Python ``True``/``False`` as well as the strings
    ``"TRUE"``, ``"FALSE"``, ``"True"``, ``"False"``, ``"true"`` and
    ``"false"`` (matching is case-insensitive).

    Args:
        value: The value to validate. May be a ``bool`` or a ``str``.
        field_name (str): Name of the field being validated.
        row_num (int): The 1-based line number in the source file.

    Returns:
        tuple[bool, str | None]: ``(True, None)`` if the value is a valid
        boolean, otherwise ``(False, "<error message>")``.

    Example:
        >>> validate_boolean("TRUE", "has_question_mark", 2)
        (True, None)
        >>> validate_boolean("maybe", "has_question_mark", 3)
        (False, "Row 3: has_question_mark 'maybe' is not a boolean value")
    """

    #Check if value is a boolean (TRUE/FALSE, True/False, true/false).
    if isinstance(value, bool):
        return True, None
    if isinstance(value, str):
        if value.upper() in ['TRUE', 'FALSE']:
            return True, None
    return False, f"Row {row_num}: {field_name} '{value}' is not a boolean value"


def validate_csv_file(file_path):
    """
    Validate every row of an enriched transcript CSV and print a report.

    Each row is checked against six rules: one timestamp validation, four
    "positive number" validations (``time_taken_sec``, ``num_words_in_text``,
    ``speech_rate_wps`` and ``speaker_counter``) and one boolean validation
    (``has_question_mark``). Any failure is collected with the source line
    number; if no failures occur, a passing summary is printed.

    Args:
        file_path (str): Path to the enriched transcript CSV.

    Returns:
        None. Results are printed to standard output.

    Complexity:
        Time  - O(n), where n is the number of rows. Each row runs a constant
                number of constant-time validators.
        Space - O(e), where e is the number of errors recorded. With no
                errors this collapses to O(1).

    Example:
        >>> validate_csv_file("group_transcript_enriched.csv")
        Validation passed!
        All 30 rows are valid.
        ...
    """
    
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
        else:
            print("Validation passed!")
            print(f"All {row_number} rows are valid.")
            print("\nSummary:")
            print(f"- Total rows checked: {row_number}")
            print(f"- All timestamps are valid")
            print(f"- All numeric fields are positive numbers")
            print(f"- All boolean fields are valid")
            print(f"- No missing required values")
                


def main():
    """
    Entry point: run the validator against the default CSV path.

    Edit ``file_path`` below if your enriched transcript is stored under a
    different name or location.
    """

    #Main function to run CSV validation.
    file_path = "group_transcript_enriched.csv"
    
    print("=" * 50)
    print("CSV Validation Report")
    print("=" * 50)
    print(f"File: {file_path}\n")
    
    validate_csv_file(file_path)


if __name__ == "__main__":
    main()