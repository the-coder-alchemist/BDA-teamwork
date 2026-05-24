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

```powershell (or command prompt CMD)
python3 --version
```

## 4. Create API key (free)

Go to Google AI Studio, login using your gmail account and create an API key:

- https://aistudio.google.com/app/api-keys
- Add a name (or keep the default) and choose `Default Gemini Project`.
- Create a key and keep it private.
- Copy the API key (for example, `AIza...`).

## 5. Set API key in terminal

Return to your Visual Studio Code terminal. On macOS/Linux, run the following command (replace with your API key):

```bash
export GEMINI_API_KEY="PASTE_YOUR_KEY"
```

On Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="PASTE_YOUR_KEY"
```

On Windows Command Prompt (CMD):

```Command Prompt
set GEMINI_API_KEY="PASTE_YOUR_KEY"
```

Two quick details to keep in mind:
Temporary Nature:
This only sets the key for your current Command Prompt session. If you close the window, you will need to run it again.

Making it permanent:
If you want Command Prompt to remember your key every time you open it, use setx instead:

setx GEMINI_API_KEY "PASTE_YOUR_KEY"

_(Note: After running `setx`, you will need to restart VS Code or open a new terminal window for the change to take effect)._

> [!TIP]
> Gemini is free to use (at the time of this writing), but there are some limits.The code provided in this repository in the (`gemini_vosk.py`) file numbers each text item and sends them to Gemini in a single prompt to minimize API calls, and returns the model's corrected version. You can also use an OPENAI_API_KEY, but you will need to change the os.environ["GEMINI_API_KEY"]

```python
#gemini transcript clean
def correct_all_text(texts):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    ...

#OpenAI transcript clean
def correct_all_text(texts):
    client = genai.Client(api_key=os.environ["OPENAI_API_KEY"])
    ...
```

**Test key is set**

Run this quick check in your terminal:

```bash
python3 -c 'import os; k=os.getenv("GEMINI_API_KEY"); print("GEMINI_API_KEY set:", bool(k)); print("Key length:", len(k) if k else 0)'
```

If `GEMINI_API_KEY set: True` appears and key length is greater than 0, your environment variable is working. Clear your terminal using `clear`, and let's proceed.

**Limits note**

Google AI Studio is free, but it has usage limits (typically 5-15 requests per minute, depending on the model).

> [!TIP]
>
> Limits depend on model and tier, and can change over time.
>
> Check the latest limits before running: https://ai.google.dev/gemini-api/docs/quota. If you exceed limits, you may receive `429` errors until quota resets.

## 6. Basics you should know

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

## 7. Create and manage a virtual environment

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

The `requirements.txt` file contains the dependencies you will need:

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

## 8. Install dependencies

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
You are now ready to proceed. You can use the `clear` command to clear the terminal (Windows command prompt CMD = cls).

---

## 9. Pipeline Execution Steps

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
  _(Note: Ensure that you change the output variable to output to the csv file shown above before running the code which creates the file when you are past the testing. The subsequent files need the csv file to be named as above to work - or you will need to find and change this name in all the files)._

```python
#Configuring Model
...
OUTPUT_CSV = "test_transcript.csv"
...

# Change to this before running the gemini_vosk.py file
#Configuring Models
...
OUTPUT_CSV = "group_transcript_enriched.csv"
...
```

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

## 10. Meeting Analytics Pipeline Test Suite (`test_pipeline_enhanced.py`)

This automated test suite provides testing and pipeline integrity checks for the conversational data processing pipeline. It utilizes virtualized in-memory file routing (`io.StringIO`) and function mocking (`unittest.mock.patch`) to evaluate file structural constraints, edge-case mathematical data updates, and report generation accuracy without modifying production data files.

### 10.1 Monitored Modules & Files Under Test

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

### 10.2 Execution Outputs

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

## 11. Complexity Analysis

This section outlines the Time and Space complexity of the primary functions and processing pipelines implemented across the scripts.

- Let **$N$** = Total number of rows (speach) in the CSV file.
- Let **$S$** = Number of unique speakers/participants ($S \le N$).
- Let **$E$** = Total number of validation errors caught ($E \le 6N$).
- Let **$L$** = Character length of text strings or speech rows.
- Let **$T$** = Total runtime duration of the live audio stream in seconds.
- Let **$W$** = Total word/character count of completed local transcript text.

### 11.1. Meeting Analytics (`analytics_stats_output.py`)

#### `analyze_meeting_data(file_path)`

- **Time Complexity:** $O(N + S^2)$
  - _Data Gathering:_ $O(N)$, where $N$ is the total number of speech text rows in the CSV file. The script streams rows sequentially and performs $O(1)$ average-time dictionary insertions and lookups.
  - _Aggregation & Metrics:_ $O(S)$, where $S$ is the number of unique speakers ($S \le N$). Finding min/max metrics requires iterating over the speaker dictionaries.
  - _Sorting:_ $O(S^2)$ due to a custom nested-loop **Bubble Sort** implementation used to rank the top 5 speakers by time.
  - _Overall:_ Since $S$ is typically very small in a meeting context, the linear file-scanning time $O(N)$ dominates under practical conditions.
- **Space Complexity:** $O(S)$
  - The file is read iteratively via `csv.DictReader`, avoiding loading the raw file into memory ($O(1)$ heap allocation for input stream).
  - Auxiliary space scales linearly with the number of unique speakers $S$ to store aggregate data structures (`word_count`, `question_count`, `speaking_time`, etc.).

---

### 11.2. Data Validation (`csv_validation.py`)

#### `validate_csv_file(file_path)`

- **Time Complexity:** $O(N)$
  - The script reads through the file line-by-line exactly once for all $N$ rows.
  - For each row, it executes a series of field-level helper validations (`validate_timestamp`, `validate_numeric_positive`, and `validate_boolean`). Each helper completes in $O(1)$ constant time.
  - Printing the final results takes $O(E)$ time, where $E$ is the total number of validation errors caught ($E \le 6N$).
- **Space Complexity:** $O(E)$ (Up to $O(N)$ in the worst case)
  - The input stream consumes $O(1)$ auxiliary memory.
  - The primary memory consumer is the `validation_errors` list. In a valid file layout, space complexity is $O(1)$. If every column in every row encounters a failure, it scales linearly to $O(N)$.

---

### 11.3. Feature Enrichment (`feature_enrichement.py`)

#### Sequential Processing Pipeline

- **Time Complexity:** $O(N \cdot L)$
  - The pipeline iterates through all $N$ rows in the input file.
  - For each record, it runs string-based checks (`'?' in text`, `.split()`, and `len()`) to enrich the dataset. These operations run in time proportional to the character length of the text string, $L$.
  - Assuming an upper-bound constant for speech row length ($L$), the operational time simplifies to a linear $O(N)$.
- **Space Complexity:** $O(S)$
  - Input and output files are read and written continuously line-by-line, keeping memory usage minimal.
  - An auxiliary tracking dictionary (`counter`) dynamically grows to match the number of unique speakers $S$ to compute the sequential speaker turn counts.

---

### 11.4. Transcription and LLM Pipeline (`gemini_vosk.py`)

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

### 11.5. Complexity Summary Table

Below is a quick reference summary of the computational complexity for each primary function across the system.

- Let **$N$** = Total number of rows (speach) in the CSV file.
- Let **$S$** = Number of unique speakers/participants ($S \le N$).
- Let **$E$** = Total number of validation errors caught ($E \le 6N$).
- Let **$L$** = Character length of text strings or speech rows.
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
