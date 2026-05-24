import io
import sys
import unittest
from unittest.mock import patch, mock_open

# Import functions from your pipeline files
import csv_validation, analytics_stats_output, feature_enrichement, gemini_vosk


# Custom stream wrapper to prevent the 'with' statement from killing our mock object data access
class NonClosingStringIO(io.StringIO):
    def close(self):
        # Do absolutely nothing when context manager calls .close()
        pass
        
    def force_close(self):
        # Allow cleanup manually if needed later
        super().close()


# Custom Test Result Tracker to gather metadata dynamically during execution
class PipelineTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        # Extract function name and the target file being evaluated
        method_name = test._testMethodName
        docstring = test.shortDescription() or "No description provided"
        
        # Map our test methods to the target source files for reporting clarity
        file_mapping = {
            "test_validate_timestamp_formats": "csv_validation.py",
            "test_validate_boolean_formats": "csv_validation.py",
            "test_numeric_positive_boundaries": "csv_validation.py",
            "test_feature_enrichment_logic": "feature_enrichement.py",
            "test_analytics_data_reporting": "analytics_stats_output.py"
        }
        target_file = file_mapping.get(method_name, "Unknown Source Module")
        self.successes.append((method_name, docstring, target_file))


class PipelineTestRunner(unittest.TextTestRunner):
    """Custom runner to hook up our tracking reporter class."""
    resultclass = PipelineTestResult


class TestPipeline(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. FILE STRUCTURAL INTEGRITY CHECKS (csv_validation.py)
    # ---------------------------------------------------------
    def test_validate_timestamp_formats(self):
        """Ensure ISO timestamps pass and malformed ones fail."""
        # Valid ISO format
        is_valid, _ = csv_validation.validate_timestamp("2026-05-23T14:30:00", "timestamp", 1)
        self.assertTrue(is_valid)

        # Invalid formats
        is_valid, err = csv_validation.validate_timestamp("23-05-2026", "timestamp", 2)
        self.assertFalse(is_valid)
        self.assertIn("not a valid datetime", err)

    def test_validate_boolean_formats(self):
        """Ensure boolean validations cleanly capture various cases."""
        # Valid variations
        self.assertTrue(csv_validation.validate_boolean("TRUE", "has_question", 1)[0])
        self.assertTrue(csv_validation.validate_boolean("false", "has_question", 2)[0])
        self.assertTrue(csv_validation.validate_boolean(True, "has_question", 3)[0])

        # Invalid variations
        is_valid, err = csv_validation.validate_boolean("Yes", "has_question", 4)
        self.assertFalse(is_valid)
        self.assertIn("not a boolean value", err)

    # ---------------------------------------------------------
    # 2. BOUNDARY VALUE CRITERIA VERIFICATION (csv_validation.py)
    # ---------------------------------------------------------
    def test_numeric_positive_boundaries(self):
        """Verify numeric boundaries (> 0 constraint)."""
        # Upper Boundary (Normal expected positive value)
        self.assertTrue(csv_validation.validate_numeric_positive("10.5", "time_taken_sec", 1)[0])

        # Exact Boundary (0 should fail because constraint is strictly > 0)
        is_valid_zero, err_zero = csv_validation.validate_numeric_positive("0", "time_taken_sec", 2)
        self.assertFalse(is_valid_zero)
        self.assertIn("not greater than 0", err_zero)

        # Negative Boundary (< 0 should fail)
        is_valid_neg, err_neg = csv_validation.validate_numeric_positive("-1", "time_taken_sec", 3)
        self.assertFalse(is_valid_neg)
        self.assertIn("not greater than 0", err_neg)

        # Non-numeric string boundary exception
        is_valid_str, err_str = csv_validation.validate_numeric_positive("abc", "time_taken_sec", 4)
        self.assertFalse(is_valid_str)
        self.assertIn("not numeric", err_str)

    # ---------------------------------------------------------
    # 3. FEATURE ENRICHMENT PIPELINE STEP (feature_enrichement.py)
    # ---------------------------------------------------------
    @patch("builtins.open")
    def test_feature_enrichment_logic(self, mock_file_open):
        """Test feature enrichment equations and row modification."""
        # 1. Raw Mock Data simulating group_transcript.csv
        csv_input = (
            "name,time_taken_sec,text\n"
            "Alice,2.0,Hello world?\n"
            "Bob,1.0,Test\n"
            "Alice,4.0,This is a longer sentence\n"
        )
        
        # 2. Create independent non-closing virtual file streams
        mock_infile = NonClosingStringIO(csv_input)
        mock_outfile = NonClosingStringIO()
        
        # 3. Smart side-effect router function
        def open_router(filename, *args, **kwargs):
            if "group_transcript_enriched.csv" in filename:
                return mock_outfile
            else:
                return mock_infile
                
        mock_file_open.side_effect = open_router

        # 4. Safely trigger your top-level script logic execution
        if "feature_enrichement" in sys.modules:
            importlib = sys.modules['importlib'] if 'importlib' in sys.modules else __import__('importlib')
            importlib.reload(sys.modules["feature_enrichement"])
        else:
            import feature_enrichement

        # 5. Rewind and extract the generated output data
        mock_outfile.seek(0)
        output_data = mock_outfile.read()
        
        # Clean up stream objects explicitly
        mock_infile.force_close()
        mock_outfile.force_close()

        # 6. Verify structural pipeline changes
        self.assertIn("has_question_mark", output_data)
        self.assertIn("speech_rate_wps", output_data)
        
        # Alice row 1 calculations: 2 words / 2.0 seconds = 1.0 wps
        self.assertIn("1.0", output_data) 
        
        # Split lines dynamically to safely strip away variable \r\n variations
        lines = output_data.splitlines()
        
        # Verify that the last row ends with the counter field matching '2'
        last_row = lines[-1]
        self.assertTrue(last_row.endswith(",2"), f"Expected line to end with target speaker count ',2', got: {last_row}")

    # ---------------------------------------------------------
    # 4. CONVERSATIONAL DATA ANALYTICS REPORTING (analytics_stats_output.py)
    # ---------------------------------------------------------
    @patch("builtins.open")
    def test_analytics_data_reporting(self, mock_file_open):
        """Verify bubble-sorting metrics and text aggregation output."""
        # Simulated Enriched Data
        enriched_mock_csv = (
            "timestamp,name,time_taken_sec,text,has_question_mark,num_words_in_text,text_size_chars,speech_rate_wps,speaker_counter\n"
            "2026-05-23T12:00:00,Alice,10.0,Question?,TRUE,1,9,0.1,1\n"
            "2026-05-23T12:01:00,Bob,5.0,Hello world,FALSE,2,11,0.4,1\n"
            "2026-05-23T12:02:00,Alice,20.0,Another longer text payload statement,FALSE,5,38,0.25,2\n"
        )
        
        mock_file_open.return_value = io.StringIO(enriched_mock_csv)

        # Redirect standard output to a string buffer to catch printed metrics
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            analytics_stats_output.analyze_meeting_data("mock_path.csv")
        finally:
            sys.stdout = sys.__stdout__ # Reset print stream redirection

            
        report = captured_output.getvalue()

        # Aggregation Check Assertions
        self.assertIn("Most words: Alice - 6 words", report)
        self.assertIn("Least words: Bob - 2 words", report)
        self.assertIn("Total speaking time: 35.0 seconds", report)
        self.assertIn("Most questions: Alice - 1 questions", report)
        self.assertIn("Alice: 30.00 seconds", report) # Max sorting validation
        self.assertIn("Bob: 5.00 seconds", report)


if __name__ == "__main__":
    # Create an execution suite containing our pipeline assertions
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPipeline)
    
    # Run tests using our tracking custom runner instead of standard unittest.main()
    runner = PipelineTestRunner(verbosity=0) # verbosity=0 silences default generic dots
    result = runner.run(suite)
    
    # Print the Final Analytics Execution Report
    print("\n" + "=" * 80)
    print("                    PIPELINE INTEGRITY & ANALYTICS REPORT                      ")
    print("=" * 80)
    print(f"Total Tests Executed: {result.testsRun}")
    print(f"Successful Passes   : {len(result.successes)}")
    print(f"Failures / Crashes  : {len(result.failures) + len(result.errors)}")
    print("-" * 80)
    
    print(f"{'TEST METHOD NAME':<35} | {'TARGET SOURCE FILE':<23} | {'VERIFICATION VERDICT'}")
    print("-" * 80)
    
    # Display successful metrics
    for method, desc, target_file in result.successes:
        print(f"{method:<35} | {target_file:<23} | PASS (✓)")
        print(f"  └─ Objective: {desc}")
        
    # Display errors if any pop up down the line
    for test, err in result.failures + result.errors:
        print(f"{test._testMethodName:<35} | ERROR/FAIL (🗙)")

    print("=" * 80)
    print("Pipeline Verification Process Complete.")
    print("=" * 80)