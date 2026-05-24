"""
Pipeline Unit Test Suite
=========================

Verifies that the four-stage meeting-transcription pipeline behaves
correctly:

    1. ``csv_validation``         - row-level format checks
    2. ``feature_enrichement``    - per-row derived columns
    3. ``analytics_stats_output`` - per-speaker aggregate report
    4. ``gemini_vosk``            - imported only to confirm it loads

The harness uses Python's standard ``unittest`` framework but customises
two pieces:

    * ``PipelineTestResult`` - records *successful* tests (and the source
      file they target) in addition to the usual failure/error tracking.
    * ``PipelineTestRunner`` - a thin subclass that wires the custom
      result class into ``TextTestRunner``.

After the suite finishes, the ``__main__`` block prints a tabular report
of every test, the pipeline file it exercised, and the verdict.

Usage:
    python pipeline_unit_testing.py
"""

# Metadata
__author__ = []
__credits__ = ["Carys Williams","Gary Murphy", "William McKenna", "Mei Len Vorkel", "Samuel Weldemariam", "Toby Lock"]
__version__ = "1.0.0"

# Custom Academic Attribution Matrix
__team__ = "The Pipeline"
__module__ = "Big Data Analytics (BUCI065H7)"
__assignment__ = "Assignment 1 - Startup Meeting Speech Analytics"

import io
import sys
import unittest
from unittest.mock import patch, mock_open

# Import functions from your pipeline files
import csv_validation, analytics_stats_output, feature_enrichement, gemini_vosk


# Custom stream wrapper to prevent the 'with' statement from killing our mock object data access
class NonClosingStringIO(io.StringIO):
    """
    A ``StringIO`` subclass whose ``close()`` is a no-op.

    The code under test wraps file objects in ``with open(...)`` blocks,
    which automatically close the file when the block exits. For a real
    file that is exactly what we want, but when the "file" is a mock
    ``StringIO``, closing it discards the captured bytes before the test
    can read them back. Overriding ``close()`` to do nothing keeps the
    buffer alive across the ``with`` block. The original close behaviour
    is still available via ``force_close()`` for explicit cleanup.

    Example:
        >>> buf = NonClosingStringIO()
        >>> with buf as f:                 # 'with' would normally close it
        ...     f.write("hello")
        5
        >>> buf.seek(0)
        0
        >>> buf.read()                     # data is still available
        'hello'
        >>> buf.force_close()              # now actually free it
    """

    def close(self):
        """
        No-op override.

        Called automatically by ``with`` blocks in the code under test;
        deliberately does nothing so that the buffer's contents remain
        accessible after the block exits.
        """

        # Do absolutely nothing when context manager calls .close()
        pass
        
    def force_close(self):
        """
        Truly close the underlying buffer.

        Call this from test teardown when the buffer is no longer needed,
        so its memory can be released.
        """

        # Allow cleanup manually if needed later
        super().close()


# Custom Test Result Tracker to gather metadata dynamically during execution
class PipelineTestResult(unittest.TextTestResult):
    """
    Custom ``TestResult`` that remembers successful tests, not just failures.

    The default ``unittest.TextTestResult`` keeps lists of ``failures`` and
    ``errors`` but only counts successes. This subclass additionally stores,
    for each passing test, a tuple of:

        (method_name, docstring, target_source_file)

    so that the post-run report in ``__main__`` can show *which* tests
    passed and *which file* each was checking.

    Attributes:
        successes (list[tuple[str, str, str]]): One entry per passing test.
    """

    def __init__(self, stream, descriptions, verbosity):
        """
        Initialise the parent result, then add an empty ``successes`` list.

        Args:
            stream: The output stream unittest writes progress to.
            descriptions (bool): Whether to print test descriptions.
            verbosity (int): 0 = quiet, 1 = dots, 2 = one line per test.
        """

        super().__init__(stream, descriptions, verbosity)
        self.successes = []

    def addSuccess(self, test):
        """
        Record a passing test along with its docstring and target file.

        Called by the runner whenever a test finishes without raising. The
        ``file_mapping`` dictionary links each test method name to the
        pipeline source file it exercises; tests not in the mapping are
        recorded as ``"Unknown Source Module"``.

        Args:
            test (unittest.TestCase): The test instance that just passed.

        Side effects:
            Appends a ``(method_name, docstring, target_file)`` tuple to
            ``self.successes``.
        """

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
    """
    ``TextTestRunner`` subclass that produces ``PipelineTestResult`` objects.

    Setting ``resultclass`` is the documented way to plug a custom result
    type into the standard runner. Apart from that, behaviour is identical
    to ``unittest.TextTestRunner``.
    """
    resultclass = PipelineTestResult


class TestPipeline(unittest.TestCase):
    """
    Test cases covering the four pipeline stages.

    Each test is grouped under a comment banner naming the source file it
    targets. The validator tests use direct calls; the enrichment and
    analytics tests use ``unittest.mock.patch`` on ``builtins.open`` to
    feed mocked CSV data without touching the disk.
    """

    # ---------------------------------------------------------
    # 1. FILE STRUCTURAL INTEGRITY CHECKS (csv_validation.py)
    # ---------------------------------------------------------
    def test_validate_timestamp_formats(self):
        """
        Ensure ISO timestamps pass and malformed ones fail.

        Verifies that ``validate_timestamp`` accepts a well-formed ISO 8601
        datetime and rejects a date written in ``DD-MM-YYYY`` form, returning
        a helpful error message that mentions "not a valid datetime".
        """

        # Valid ISO format
        is_valid, _ = csv_validation.validate_timestamp("2026-05-23T14:30:00", "timestamp", 1)
        self.assertTrue(is_valid)

        # Invalid formats
        is_valid, err = csv_validation.validate_timestamp("23-05-2026", "timestamp", 2)
        self.assertFalse(is_valid)
        self.assertIn("not a valid datetime", err)

    def test_validate_boolean_formats(self):
        """
        Ensure boolean validation accepts known forms and rejects others.

        Confirms that ``validate_boolean`` treats ``"TRUE"``, ``"false"``
        and the native ``True`` as valid, and rejects ``"Yes"`` with a
        message that mentions "not a boolean value".
        """

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
        """
        Verify the ``> 0`` constraint at its boundary cases.

        Checks four points:
            * ``"10.5"`` - a normal positive value, should pass.
            * ``"0"``    - the exact boundary, should fail because the
              constraint is strictly greater than zero.
            * ``"-1"``   - clearly negative, should fail.
            * ``"abc"``  - non-numeric, should fail with a "not numeric"
              message rather than a comparison-based message.
        """

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
        """
        Test feature-enrichment equations and per-row column additions.

        Replaces ``builtins.open`` with a router that returns two
        ``NonClosingStringIO`` buffers - one preloaded with three mock
        input rows, one empty for capturing output. Reloads
        ``feature_enrichement`` so its top-level code runs against the
        mocks, then verifies:

            * the new columns ``has_question_mark`` and ``speech_rate_wps``
              appear in the header row
            * Alice's first row produces ``"1.0"`` words per second
              (2 words / 2.0 seconds)
            * Alice's *second* row is correctly tagged as her 2nd
              utterance via the ``speaker_counter`` column

        Compatibility note:
            This test assumes ``feature_enrichement.py`` performs the
            enrichment as a top-level side effect of being imported. If
            the enrichment is moved into a function behind an
            ``if __name__ == "__main__"`` guard, this test must call
            that function explicitly instead of relying on the reload.
        """

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
            """Return the output buffer for the enriched path, input buffer otherwise."""

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
        """
        Verify bubble-sorting metrics and text aggregation output.
        Verify per-speaker aggregation and the sorted top-speaker output.

        Feeds ``analyze_meeting_data`` a mocked enriched CSV with three
        rows (Alice twice, Bob once) by patching ``builtins.open`` and
        redirecting ``sys.stdout`` to a buffer. Then checks the captured
        report contains the expected aggregates:

            * Alice has the most words (1 + 5 = 6)
            * Bob has the fewest words (2)
            * Total speaking time is 35.0 seconds (10 + 5 + 20)
            * Alice asked the only question
            * The sort places Alice (30.00s) above Bob (5.00s) in the
              "top speakers by total time" section
        """

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