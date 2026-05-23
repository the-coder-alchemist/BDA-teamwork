# Team Pipeline Project: Meeting Speech Analytics with Vosk + AI

---

## 1. Project Overview

This repository contains a data analytics pipeline designed for team meeting speech processing. The application records microphone audio data during real-time conversations, streams transcription tasks using an open-source speech-to-text model, cleans spelling errors via LLM (Large Language Model) API integration, calculates downstream speaking behaviour statistics with native Python routines, validates schema bounds, and prints finalised executive performance summaries.

The architecture ensures that teams can seamlessly clone this repository, install required libraries, and record, validate, and extract conversational intelligence.

---

## 2. Workspace setup

1. Install Git if it is not already installed from [here](https://git-scm.com/install/). For Mac: `brew install git`. For Windows: download and install it.
2. Install [Visual Studio Code](https://code.visualstudio.com/) (or another editor you prefer). After installing Git, restart VS Code if it was already open.
3. Open a terminal.
4. Clone the class repository:

```bash
git clone https://github.com/the-coder-alchemist/BDA-teamwork.git
```

> [!TIP]
>
> If the repository already exists, run `git pull` instead of cloning again.

5. Open the project folder in VS Code.
6. Open a terminal inside VS Code. (File Menu > Terminal > New Terminal)
7. You will need to navigate to folders using the `cd` command.

## 3. Check Python installation

Check that Python is installed:

```bash
python3 --version
```

On Windows, you can also run:

```powershell (or CMD)
python3 --version
```

## 4. Basics you should know

- `Python`: the programming language, not the snake 🐍.

- `Terminal`: a text-based tool where you run commands like `python3 --version` or `pip install`.
- `cd`: changes directory (moves you into another folder).
- `pwd`: prints your current folder path.
- `Virtual environment (.venv)`: keeps each project’s Python packages separate, so different projects don’t conflict. Different projects often need different package versions; isolation avoids conflicts.
- `pip`: Python’s package manager; it installs libraries like `vosk` or `sounddevice`.
- `requirements.txt`: a list of required Python packages for the project. It lets everyone install the same dependencies and reproduce the same setup. (Recommended: Use a virtual environment run this. See instructions below)
- `README.md`: a simple project file where you document what you built, what worked, and what is pending (useful for tracking progress). Not sure about Markdown syntax? [Check here](https://www.markdownguide.org/basic-syntax/).

You will need to navigate folders in the terminal using `cd`.

Quick examples (macOS/Linux):

```bash
pwd
cd session1
pwd
cd ..
```

Quick examples (Windows PowerShell):

```powershell
Get-Location
cd session1
Get-Location
cd ..
```

## 5. Create and manage a virtual environment

You will need a virtual environment to install the required packages.

> [!TIP]
>
> Make sure you are in the correct folder before creating it.
>
> Navigate to the folder using `cd BDA-teamwork`.

Create a virtual environment:

On macOS/Linux(the dot before the name hides the folder):

```bash
python3 -m venv .venv
```

On Windows:

```powershell
python -m venv .venv
# or
py -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

> On Windows (VS Code terminal):
>
> - PowerShell: `.venv\Scripts\Activate.ps1` (may be blocked by execution policy on some machines. Then use CMD, navigate to the Scripts folder and enter activate)
> - If activation is blocked, run scripts directly with: `.venv\Scripts\python.exe your_script.py`

Deactivate it when needed:

```bash
deactivate
```

Now check the `requirements.txt` file. It contains the dependencies we need:

```txt
google-auth==2.50.0
google-genai==1.75.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.13
pyasn1==0.6.3
pyasn1_modules==0.4.2
pycparser==3.0
pydantic==2.13.3
pydantic_core==2.46.3
requests==2.33.1
sniffio==1.3.1
sounddevice==0.5.5
srt==3.5.3
tenacity==9.1.4
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
urllib3==2.6.3
vosk==0.3.44
websockets==16.0
```

> [!TIP]
>
> A **`requirements.txt`** file lists all Python packages a project needs. It helps everyone recreate the same environment. Pin exact versions when reproducibility is critical.

## 6. Install dependencies

Activate `.venv` again and install dependencies:

```bash
pip install -r requirements.txt
```

If `pip` is missing, run:

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
```

Check the output to ensure everything installed successfully.
You are now ready to proceed. You can use the `clear` command to clear the terminal (Windows CMD = cls). Try it out.

---

## 7. Pipeline Execution Steps

The analytics pipeline contains the following algorithmic stages:

### Stage 1: Record and transcribe speech (`gemini_vosk.py`)

Record each speaker turn and save a raw CSV row. Example raw data:

| timestamp                    | name            | raw_text_vosk                                                                                          | time_taken_sec |
| ---------------------------- | --------------- | ------------------------------------------------------------------------------------------------------ | -------------- |
| `2026-05-10T12:59:12.495072` | Carys Williams  | `i've been tracking use a sign ups and while they're up the conversion from free to pay is low`        | `8.26`         |
| `2026-05-10T12:59:27.960636` | William McKenna | `i think the onboarding flow is the bottle neck is currently taking users too long to find the valley` | `10.07`        |
| `2026-05-10T12:59:42.62123`  | Gary Murphy     | `that's a fair points caris what does the pricing feedback look like from those early users`           | `8.1`          |

### Stage 2: Correct the Transcript With AI (`gemini_vosk.py`)

Send each `raw_text_vosk` value to Gemini. The AI should correct spelling, punctuation, and readability. It should not change the meaning.

Example corrected data:

| timestamp                    | name               | raw_text_vosk                                                                                      | text                                                                                                   | time_taken_sec |
| ---------------------------- | ------------------ | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------- |
| `2026-05-10T13:01:15.176884` | Toby Lock          | `of allocated budget for the security audit but we need to decide if we're hiring more developers` | `I've allocated budget for the security audit, but we need to decide if we're hiring more developers.` | `9.24`         |
| `2026-05-10T13:01:44.795188` | Mei Len Vorkel     | `we definitely need of back and specialist if we plan on horizontal scaling by careful`            | `We definitely need a backend specialist if we plan on horizontal scaling. But be careful`             | `8.33`         |
| `2026-05-10T13:02:07.814951` | Samuel Weldemariam | `if we hire know i can start building the brand story around on new speed and security focus`      | `If we hire now, I can start building the brand story around our new speed and security focus`         | `8.96`         |

### Stage 3: Enrich the Dataset With Python (`feature_enrichement.py`)

Python logic, not AI, is used to add calculated columns.

| Column Name       | Column Calculation                                                      |
| ----------------- | ----------------------------------------------------------------------- |
| `timestamp`       | Keep from the raw data.                                                 |
| `name`            | Keep from the raw data.                                                 |
| `raw_text_vosk`   | Keep from the raw data.                                                 |
| `text`            | AI-corrected transcript.                                                |
| `time_taken_sec`  | Keep from the raw data.                                                 |
| `question_flag`   | `True` if `text` ends with `?`, otherwise `False`.                      |
| `num_words`       | Number of words in `text`.                                              |
| `text_size_chars` | Number of characters in `text`.                                         |
| `speech_rate_wps` | `num_words / time_taken_sec`, rounded sensibly.                         |
| `speaker_counter` | Running count for each speaker: first turn is 1, second turn is 2, etc. |

- Reads the corrected log data and applies programmatic rules to output a performance-optimized output file (`group_transcript_enriched.csv`).
- Calculations bypass deep models to avoid unnecessary AI processing costs:
  - **`has_question_mark`**: Triggers a boolean `True`/`False` check based on trailing syntax.
  - **`num_words_in_text`**: Computes standard splits over whitespace.
  - **`text_size_chars`**: Returns absolute lengths via string measuring logic.
  - **`speech_rate_wps`**: Returns calculated words spoken divided by duration values (`num_words_in_text / time_taken_sec`), rounded to 2 decimal places.
  - **`speaker_counter`**: Evaluates individual dynamic historical indices to track speaking order (`speaker_counter`).

### Stage 4: Validate the CSV (`csv_validation.py`)

Before analytics, the code checks that the final CSV is usable (the CSV has at least 25 rows).

The code checks the following:

- No required values are missing.
- `timestamp` values can be parsed as dates/times.
- `time_taken_sec` is numeric and greater than 0.
- `num_words` is numeric and greater than 0.
- `speech_rate_wps` is numeric and greater than 0.
- `question_flag` contains boolean values.
- `speaker_counter` is numeric and greater than 0

Validation will print clear messages. For example:

```text
Validation failed:
- Row 4: timestamp "-04-28T10:00:05" is not a valid datetime.
- Row 3: speech_rate_wps is missing.
```

### Stage 5: Analyse the Dataset (`analytics_stats_output.py`)

- Summarizes performance attributes using a built-in Bubble Sort implementation to calculate rankings, determine speech velocities, and identify leading participants.

After validation passes, the following questions are answered:

1. Who spoke the most by total words?
2. Who spoke the least by total words?
3. What is the total speaking time of the meeting?
4. What is the average speaking time per speaker?
5. Who asked the most questions?
6. Who are the top 5 speakers by total speaking time?
7. What is each speaker's average speech rate?

The following is an example analytics output for the valid rows above:

```text
==================================================
Meeting Analytics Report
==================================================

Most words: Gary Murphy - 109 words
Least words: Toby Lock - 63 words
Total speaking time: 259.39 seconds
Average speaking time per speaker: 43.23 seconds
Most questions: Gary Murphy - 4 questions

Top 5 speakers by total time:
Gary Murphy: 60.89 seconds
William McKenna: 46.76 seconds
Carys Williams: 41.33 seconds
Mei Len Vorkel: 38.30 seconds
Samuel Weldemariam: 37.68 seconds

Gary Murphy average speech rate: 1.81 words/second
Carys Williams average speech rate: 1.82 words/second
William McKenna average speech rate: 1.91 words/second
Mei Len Vorkel average speech rate: 2.07 words/second
Samuel Weldemariam average speech rate: 1.86 words/second
Toby Lock average speech rate: 1.83 words/second

==================================================
```

---

## 8. Meeting Analytics Pipeline Test Suite (`test_pipeline_enhanced.py`)

This automated test suite provides testing and pipeline integrity checks for the conversational data processing pipeline. It utilizes virtualized in-memory file routing (`io.StringIO`) and function mocking (`unittest.mock.patch`) to evaluate file structural constraints, edge-case mathematical data updates, and report generation accuracy without modifying production data files.

### 8.1 Monitored Modules & Files Under Test

The script actively orchestrates unit tests and behavioural validation across the following pipeline assets:

- **`csv_validation.py`**
  - **Timestamp Format Verification:** Ensures meeting logs accurately follow strict ISO-8601 formatting criteria.
  - **Data Integrity Checkpoints:** Confirms data field inputs are accurately restricted to expected string/boolean flags (`TRUE`/`FALSE`).
  - **Boundary Value Analytics:** Confirms that numeric attributes (e.g., speech duration) conform to operational logical limits ($> 0$).
- **`feature_enrichement.py`**
  - **Mathematical Transforms:** Evaluates the runtime accuracy of feature calculations including text length counts, dynamic conversation speech-rate equations, and targeted question mark identifiers.
  - **State Tracking Logic:** Validates sequential index counters that increment individual speaker dialogue turns accurately.
- **`analytics_stats_output.py`**
  - **Sorting Validation:** Intercepts console print streams to verify that custom bubble-sorting algorithms cleanly rank meeting participants by total talk time.
  - **Aggregation Integrity:** Assures the correct derivation of metrics like average speaking speeds, question metrics, and high/low word limits.
- **`gemini_vosk.py`**
  - Imported into the pipeline workspace scope to ensure architectural integration, dependencies, and environment configurations resolve correctly during automated testing loops.

### 8.2 Execution Outputs

Console-based **Pipeline Integrity & Analytics Report**, detailing every individual test function name, its specific architectural file target, and the final verification verdict (`PASS` or `FAIL`).

Here is an example of the possible output:

```text
================================================================================
                    PIPELINE INTEGRITY & ANALYTICS REPORT
================================================================================
Total Tests Executed: 5
Successful Passes   : 5
Failures / Crashes  : 0
--------------------------------------------------------------------------------
TEST METHOD NAME                    | TARGET SOURCE FILE      | VERIFICATION VERDICT
--------------------------------------------------------------------------------
test_analytics_data_reporting       | analytics_stats_output.py | PASS (✓)
  └─ Objective: Verify bubble-sorting metrics and text aggregation output.
test_feature_enrichment_logic       | feature_enrichement.py  | PASS (✓)
  └─ Objective: Test feature enrichment equations and row modification.
test_numeric_positive_boundaries    | csv_validation.py       | PASS (✓)
  └─ Objective: Verify numeric boundaries (> 0 constraint).
test_validate_boolean_formats       | csv_validation.py       | PASS (✓)
  └─ Objective: Ensure boolean validations cleanly capture various cases.
test_validate_timestamp_formats     | csv_validation.py       | PASS (✓)
  └─ Objective: Ensure ISO timestamps pass and malformed ones fail.
================================================================================
Pipeline Verification Process Complete.
================================================================================
```

---

## 9. Algorithmic Complexity Analysis

This section provides a comprehensive breakdown of the time and space complexities for the core modules within the meeting speech analytics pipeline. Understanding these complexities ensures the system remains performant and scalable as the size of meeting transcripts and team sizes grow.

---

### 9.1 Transcription & AI Correction Pipeline (`gemini_vosk.py`)

This module manages the runtime audio recording via Vosk, stream processing into raw text, and batch text refinement utilizing the Gemini API.

- **$N$** = Total number of rows in the CSV file
- **$M$** = Average character length of speaker transcripts
- **$S$** = Number of unique speakers present in the meeting
- **$E$** = Total number of logged dataset validation errors

### `correct_all_text(texts)`

- **Time Complexity:** $O(N \cdot M)$
  _where $N$ is the total number of text segments (rows) and $M$ is the average character length of each segment._ The function programmatically joins all input text fragments into a single structured, numbered prompt string, scaling linearly with the total volume of characters $O(N \cdot M)$. The single batch API call's processing overhead on the remote Large Language Model depends directly on token counts, which scale linearly with the input volume.
- **Space Complexity:** $O(N \cdot M)$
  The application creates and holds the consolidated `numbered` prompt string and the corresponding full-text `response.text` string concurrently within memory.

### `realtime_transcription()`

- **Time Complexity:** $O(T)$
  _where $T$ is the total duration of the recorded audio._ Audio packets are captured and handled in real-time. Vosk’s underlying `KaldiRecognizer` processes incoming audio frames at a fixed, constant rate directly relative to the active runtime of the recording.
- **Space Complexity:** $O(T)$
  While the shared frame queue handles small transient memory buffers, the aggregate string `full_text` dynamically grows in memory linearly based on the amount of speech generated across duration $T$.

### `main()` Execution & Data Mapping

- **Time Complexity:** $O(N \cdot M)$
  Disk I/O operations for reading and writing the CSV scale linearly with the size of the dataset $O(N \cdot M)$. Parsing the returned batch response back into individual rows using list comprehension scales linearly with rows $O(N)$.
- **Space Complexity:** $O(N \cdot M)$
  The Pandas DataFrame dynamically allocates memory to load and manipulate the entire tabular transcript dataset at runtime.

---

### 9.2 Text Feature Enrichment (`feature_enrichement.py`)

This script extracts metrics and runs structural transformations purely using native Python logic, processing data from the raw CSV and exporting it to an enriched output format.

- **Time Complexity:** $O(N \cdot M)$
  _where $N$ is the number of rows (speaker turns) and $M$ is the average string length of text per row._ \* The top-level iteration block processes the dataset sequentially row by row, resulting in $O(N)$ passes.
  - The operation `row.get('text', '').split()` instantiates a token list by scanning a string of length $M$, requiring $O(M)$ steps.
  - Average hash-map / dictionary insertions and lookups to update tracking counters take $O(1)$ stable time.
- **Space Complexity:** $O(S)$
  _where $S$ is the total number of unique speakers in the meeting._ Because data is stream-processed sequentially using `csv.DictReader` and `csv.DictWriter`, rows are not cached in memory collectively ($O(1)$ row buffer). The primary memory consumer is the `counter` dictionary, which stores a single integer value per unique speaker.

---

### 9.3 Data Validation Engine (`csv_validation.py`)

This module evaluates the structural integrity and data types of the enriched dataset prior to executing aggregation metrics.

#### Rule Evaluation Helpers (`validate_timestamp`, `validate_numeric_positive`, `validate_boolean`)

- **Time Complexity:** $O(1)$
  Validates individual values using constant-time string parsing, type assertions, or exception handling.
- **Space Complexity:** $O(1)$
  Executes logic strictly within localized, static memory boundaries.

#### `validate_csv_file(file_path)`

- **Time Complexity:** $O(N)$
  _where $N$ is the total row count in the target CSV file._ The validation routine scans through the file line-by-line exactly once, executing an identical set of $O(1)$ rule helpers on every row.
- **Space Complexity:** $O(E)$
  _where $E$ is the count of anomalous records generating validation errors._ For clean datasets, space complexity scales at $O(1)$. If structural errors are found, messages compile linearly inside the `validation_errors` array.

---

### 9.4 Meeting Analytics & Aggregation (`analytics_stats_output.py`)

This component maps text variables into multi-dimensional metrics to produce the final analytical summary report.

#### Data Aggregation Loop

- **Time Complexity:** $O(N \cdot M)$
  The entry loop reads through all $N$ data rows sequentially. Splitting or casting strings to numerical types scales with character length $M$. Key insertions, lookups, and scalar mathematical additions inside tracking dictionaries (`word_count`, `speaking_time`, etc.) operate at an average complexity of $O(1)$.
- **Space Complexity:** $O(S)$
  The data structure registers exactly five independent tracking dictionaries, all strictly bounded by the count of unique meeting participants $S$.

#### Ranking & Report Generation

- **Time Complexity:** $O(S^2)$
  _where $S$ is the count of unique meeting participants._ \* Locating standard extrema values (e.g., maximum words, minimum words, most questions asked) utilizes simple single-pass loops traversing at $O(S)$ time.
  - Generating the **Top 5 Speakers by Time** ranking converts the dictionary into an array and runs a nested **Bubble Sort** implementation. This establishes a mathematical worst-case processing footprint of $O(S^2)$. _(Note: While quadratically inefficient for massive scales, $S$ remains extremely small for business meetings, optimizing practical execution)._
- **Space Complexity:** $O(S)$
  Required to instantiate the localized list of tuples (`speaking_time_list`) derived from the primary metrics dictionary to facilitate the inline sorting sequence.

---

### Summary Matrix

| Script / Process             | Time Complexity         | Space Complexity | Primary Resource Driver                                                          |
| :--------------------------- | :---------------------- | :--------------- | :------------------------------------------------------------------------------- |
| **`correct_all_text`**       | $O(N \cdot M)$          | $O(N \cdot M)$   | Prompt compilation payload and API token stream buffering.                       |
| **`feature_enrichement`**    | $O(N \cdot M)$          | $O(S)$           | Linear row stream tokenization; speaker tracker dictionary scaling.              |
| **`csv_validation`**         | $O(N)$                  | $O(E)$ or $O(1)$ | Single-pass file scanning; error logs compilation.                               |
| **`analytics_stats_output`** | $O(N \cdot M) + O(S^2)$ | $O(S)$           | Linear dataset reduction followed by a quadratic Bubble Sort on unique speakers. |

- **$N$** = Total number of rows in the CSV file
- **$M$** = Average character length of speaker transcripts
- **$S$** = Number of unique speakers present in the meeting
- **$E$** = Total number of logged dataset validation errors

```

```

---

## 9. Complexity Analysis

This section outlines the Time and Space complexity of the primary functions and processing pipelines implemented across the scripts.

### 9.1. Meeting Analytics (`analytics_stats_output.py`)

#### `analyze_meeting_data(file_path)`

- **Time Complexity:** $O(N + S^2)$
  - _Data Gathering:_ $O(N)$, where $N$ is the total number of utterance rows in the CSV file. The script streams rows sequentially and performs $O(1)$ average-time dictionary insertions and lookups.
  - _Aggregation & Metrics:_ $O(S)$, where $S$ is the number of unique speakers ($S \le N$). Finding min/max metrics requires iterating over the speaker dictionaries.
  - _Sorting:_ $O(S^2)$ due to a custom nested-loop **Bubble Sort** implementation used to rank the top 5 speakers by time.
  - _Overall:_ Since $S$ is typically very small in a meeting context, the linear file-scanning time $O(N)$ dominates under practical conditions.
- **Space Complexity:** $O(S)$
  - The file is read iteratively via `csv.DictReader`, avoiding loading the raw file into memory ($O(1)$ heap allocation for input stream).
  - Auxiliary space scales linearly with the number of unique speakers $S$ to store aggregate data structures (`word_count`, `question_count`, `speaking_time`, etc.).

---

### 9.2. Data Validation (`csv_validation.py`)

#### `validate_csv_file(file_path)`

- **Time Complexity:** $O(N)$
  - The script reads through the file line-by-line exactly once for all $N$ rows.
  - For each row, it executes a series of field-level helper validations (`validate_timestamp`, `validate_numeric_positive`, and `validate_boolean`). Each helper completes in $O(1)$ constant time.
  - Printing the final results takes $O(E)$ time, where $E$ is the total number of validation errors caught ($E \le 6N$).
- **Space Complexity:** $O(E)$ (Up to $O(N)$ in the worst case)
  - The input stream consumes $O(1)$ auxiliary memory.
  - The primary memory consumer is the `validation_errors` list. In a valid file layout, space complexity is $O(1)$. If every column in every row encounters a failure, it scales linearly to $O(N)$.

---

### 9.3. Feature Enrichment (`feature_enrichement.py`)

#### Sequential Processing Pipeline

- **Time Complexity:** $O(N \cdot L)$
  - The pipeline iterates through all $N$ rows in the input file.
  - For each record, it runs string-based checks (`'?' in text`, `.split()`, and `len()`) to enrich the dataset. These operations run in time proportional to the character length of the text string, $L$.
  - Assuming an upper-bound constant for utterance length ($L$), the operational time simplifies to a linear $O(N)$.
- **Space Complexity:** $O(S)$
  - Input and output files are read and written continuously line-by-line, keeping memory usage minimal.
  - An auxiliary tracking dictionary (`counter`) dynamically grows to match the number of unique speakers $S$ to compute the sequential speaker turn counts.

---

### 9.4. Transcription and LLM Pipeline (`gemini_vosk.py`)

#### `correct_all_text(texts)`

- **Time Complexity:** $O(L_{\text{total}}) + O(\text{API Call Latency})$
  - Constructing the indexed prompt string via list comprehensions requires iterating through all texts, taking linear time relative to the total length of all characters combined ($L_{\text{total}}$).
  - The transcript post-processing relies on a remote generative AI model, meaning local execution blocks on network I/O and external LLM inference processing.
- **Space Complexity:** $O(L_{\text{total}})$
  - Requires holding the full concatenated payload prompt string and the corresponding text responses in memory concurrently before parsing.

#### `realtime_transcription()`

- **Time Complexity:** $O(T)$
  - Runs an asynchronous thread loop that blocks on audio hardware inputs. The audio data buffers are fed into a local Vosk Kaldi speech recognizer via `AcceptWaveform()`.
  - Speech processing workloads scale linearly with respect to the total tracking duration of the audio segment ($T$) in seconds.
- **Space Complexity:** $O(W)$
  - The sound processing streaming queue acts as a sliding-window buffer requiring $O(1)$ constant space.
  - The continuous string collection array (`full_text`) grows linearly over time with respect to the total number of transcribed characters ($W$).

#### `main()` Execution Flow (Pandas Integration)

- **Time Complexity:** $O(N \cdot L) + O(\text{API Call Latency})$
  - Unlike the streaming implementations found in other modules, this script uses `pd.read_csv()` to load the complete history dataset into memory, taking $O(N \cdot L)$ time.
  - Splitting and mapping the structured Gemini array outputs back to matching data frames scales linearly with the size of the file.
- **Space Complexity:** $O(N \cdot L)$
  - Loads the entire transcription matrix into an in-memory Pandas `DataFrame` object structure rather than operating row-by-row, requiring memory directly proportional to the size of the dataset.

### 9.5. Complexity Summary Table

Below is a quick reference summary of the computational complexity for each primary function across the system.

- Let **$N$** = Total number of rows (speach) in the CSV file.
- Let **$S$** = Number of unique speakers/participants ($S \le N$).
- Let **$E$** = Total number of validation errors caught ($E \le 6N$).
- Let **$L$** = Character length of text strings or utterances.
- Let **$T$** = Total runtime duration of the live audio stream in seconds.
- Let **$W$** = Total word/character count of completed local transcript text.

| Script / Context              | Function or Process               | Time Complexity                               | Space Complexity      | Notes / Bottlenecks                                                                          |
| :---------------------------- | :-------------------------------- | :-------------------------------------------- | :-------------------- | :------------------------------------------------------------------------------------------- |
| **analytics_stats_output.py** | `analyze_meeting_data(file_path)` | $O(N + S^2)$                                  | $O(S)$                | Streams data line-by-line; $O(S^2)$ is introduced by the custom bubble sort implementation.  |
| **csv_validation.py**         | `validate_csv_file(file_path)`    | $O(N)$                                        | $O(E)$                | Processes row-by-row. Worst-case memory is $O(N)$ if every check fails on every row.         |
|                               | `validate_timestamp`              | $O(1)$                                        | $O(1)$                | Built-in string format parsing.                                                              |
|                               | `validate_numeric_positive`       | $O(1)$                                        | $O(1)$                | Simple float type casting and boundary checks.                                               |
|                               | `validate_boolean`                | $O(1)$                                        | $O(1)$                | Exact string set matching.                                                                   |
| **feature_enrichement.py**    | Script Pipeline Execution         | $O(N \cdot L)$                                | $O(S)$                | Line-by-line streaming. String splitting scales with sentence word length $L$.               |
| **gemini_vosk.py**            | `correct_all_text(texts)`         | $O(L_{\text{total}}) + O(\text{API Latency})$ | $O(L_{\text{total}})$ | Bound by prompt formatting overhead and remote network I/O block times.                      |
|                               | `realtime_transcription()`        | $O(T)$                                        | $O(W)$                | CPU-bound to acoustic length processing. Running string accumulates tokens over time.        |
|                               | `save_to_csv(data)`               | $O(1)$                                        | $O(1)$                | Constant time direct append-to-file operation.                                               |
|                               | `main()` Pipeline (Pandas flow)   | $O(N \cdot L) + O(\text{API Latency})$        | $O(N \cdot L)$        | **Memory Bottleneck**: Loads full datasets into an in-memory DataFrame instead of streaming. |
