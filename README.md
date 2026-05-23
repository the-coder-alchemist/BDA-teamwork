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

### Stage 1 & 2: Record, Transcribe, and AI-Correct (`gemini_vosk.py`)

- **Transcription Strategy:** Uses the `sounddevice` package to read raw mono audio input frames inside an asynchronous queue buffer stream.
- **Local Acoustic Engine:** Feeds buffers blockwise into the `vosk.KaldiRecognizer` machine (`vosk-model-en-us-0.22-lgraph`), aggregating fragmented JSON chunks into a unified `raw_text_vosk` log string.
- **AI Semantic Alignment:** Groups strings systematically and dispatches batch-indexed correction arrays to `gemini-2.5-flash-lite` through the `google-genai` client. A structured prompt ensures the model injects punctuation, fixes syntax gaps, fixes capitalization variations, and matches raw indices without changing semantic context. The results are written back to an intermediate file (`group_transcript.csv`). The OUTPUT_CSV variable in the `gemini_vosk.py` python file currently writes to a test CSV file (`test_transcript.csv`) to prevent anyone from accidentally overwriting the group transcript CSV file. Change this variable's value in the cloned repository to output to (`group_transcript.csv`) for the subsequent code to work.

### Stage 3: Dataset Feature Enrichment (`feature_enrichement.py`)

- Reads the corrected log data and applies programmatic rules to output a performance-optimized output file (`group_transcript_enriched.csv`).
- Calculations bypass deep models to avoid unnecessary processing costs:
  - **`has_question_mark`**: Triggers a boolean `True`/`False` check based on trailing syntax.
  - **`num_words_in_text`**: Computes standard splits over whitespace.
  - **`text_size_chars`**: Returns absolute lengths via string measuring logic.
  - **`speech_rate_wps`**: Returns calculated words spoken divided by duration values (`num_words_in_text / time_taken_sec`), rounded to 2 decimal places.
  - **`speaker_counter`**: Evaluates individual dynamic historical indices to track speaking order (`speaker_turn_id`).

### Stage 4: Strict CSV Validation (`csv_validation.py`)

- Evaluates constraints on row limits (verifying at least 25 entries), data type compliance, zero bounds, and logical flags before triggering analytics. Missing fields or structural breaks generate alerts detailing the exact row and problem.

### Stage 5: Analytical Reporting Engine (`analytics_stats_output.py`)

- Summarizes performance attributes using a built-in Bubble Sort implementation to calculate rankings, determine speech velocities, find structural trends, and identify leading participants.

## 8. Meeting Analytics Pipeline Test Suite (`test_pipeline_enhanced.py`)

This automated test suite provides regression testing and pipeline integrity checks for the conversational data processing pipeline. It utilizes virtualized in-memory file routing (`io.StringIO`) and function mocking (`unittest.mock.patch`) to evaluate file structural constraints, edge-case mathematical data updates, and report generation accuracy without modifying production data files.

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

---

## 9. Algorithmic Complexity Analysis

This document provides a comprehensive breakdown of the time and space complexities for the core modules within the meeting speech analytics pipeline. Understanding these complexities ensures the system remains performant and scalable as the size of meeting transcripts and team sizes grow.

---

### 9.1 Transcription & AI Correction Pipeline (`gemini_vosk.py`)

This module manages the runtime audio recording via Vosk, stream processing into raw text, and batch text refinement utilizing the Gemini API.

- **$N$** = Total number of rows in the CSV file
- **$M$** = Average character length of speaker transcripts
- **$S$** = Number of unique speakers present in the meeting
- **$E$** = Total number of logged dataset validation errors

### `correct_all_text(texts)`

- **Time Complexity:** $\mathcal{O}(N \cdot M)$  
  _where $N$ is the total number of text segments (rows) and $M$ is the average character length of each segment._ The function programmatically joins all input text fragments into a single structured, numbered prompt string, scaling linearly with the total volume of characters $\mathcal{O}(N \cdot M)$. The single batch API call's processing overhead on the remote Large Language Model depends directly on token counts, which scale linearly with the input volume.
- **Space Complexity:** $\mathcal{O}(N \cdot M)$  
  The application creates and holds the consolidated `numbered` prompt string and the corresponding full-text `response.text` string concurrently within memory.

### `realtime_transcription()`

- **Time Complexity:** $\mathcal{O}(T)$  
  _where $T$ is the total duration of the recorded audio._ Audio packets are captured and handled in real-time. Vosk’s underlying `KaldiRecognizer` processes incoming audio frames at a fixed, constant rate directly relative to the active runtime of the recording.
- **Space Complexity:** $\mathcal{O}(T)$  
  While the shared frame queue handles small transient memory buffers, the aggregate string `full_text` dynamically grows in memory linearly based on the amount of speech generated across duration $T$.

### `main()` Execution & Data Mapping

- **Time Complexity:** $\mathcal{O}(N \cdot M)$  
  Disk I/O operations for reading and writing the CSV scale linearly with the size of the dataset $\mathcal{O}(N \cdot M)$. Parsing the returned batch response back into individual rows using list comprehension scales linearly with rows $\mathcal{O}(N)$.
- **Space Complexity:** $\mathcal{O}(N \cdot M)$  
  The Pandas DataFrame dynamically allocates memory to load and manipulate the entire tabular transcript dataset at runtime.

---

### 9.2 Text Feature Enrichment (`feature_enrichement.py`)

This script extracts metrics and runs structural transformations purely using native Python logic, processing data from the raw CSV and exporting it to an enriched output format.

- **Time Complexity:** $\mathcal{O}(N \cdot M)$  
  _where $N$ is the number of rows (speaker turns) and $M$ is the average string length of text per row._ \* The top-level iteration block processes the dataset sequentially row by row, resulting in $\mathcal{O}(N)$ passes.
  - The operation `row.get('text', '').split()` instantiates a token list by scanning a string of length $M$, requiring $\mathcal{O}(M)$ steps.
  - Average hash-map / dictionary insertions and lookups to update tracking counters take $\mathcal{O}(1)$ stable time.
- **Space Complexity:** $\mathcal{O}(S)$  
  _where $S$ is the total number of unique speakers in the meeting._ Because data is stream-processed sequentially using `csv.DictReader` and `csv.DictWriter`, rows are not cached in memory collectively ($\mathcal{O}(1)$ row buffer). The primary memory consumer is the `counter` dictionary, which stores a single integer value per unique speaker.

---

### 9.3 Data Validation Engine (`csv_validation.py`)

This module evaluates the structural integrity and data types of the enriched dataset prior to executing aggregation metrics.

#### Rule Evaluation Helpers (`validate_timestamp`, `validate_numeric_positive`, `validate_boolean`)

- **Time Complexity:** $\mathcal{O}(1)$  
  Validates individual values using constant-time string parsing, type assertions, or exception handling.
- **Space Complexity:** $\mathcal{O}(1)$  
  Executes logic strictly within localized, static memory boundaries.

#### `validate_csv_file(file_path)`

- **Time Complexity:** $\mathcal{O}(N)$  
  _where $N$ is the total row count in the target CSV file._ The validation routine scans through the file line-by-line exactly once, executing an identical set of $\mathcal{O}(1)$ rule helpers on every row.
- **Space Complexity:** $\mathcal{O}(E)$  
  _where $E$ is the count of anomalous records generating validation errors._ For clean datasets, space complexity scales at $\mathcal{O}(1)$. If structural errors are found, messages compile linearly inside the `validation_errors` array.

---

### 9.4 Meeting Analytics & Aggregation (`analytics_stats_output.py`)

This component maps text variables into multi-dimensional metrics to produce the final analytical summary report.

#### Data Aggregation Loop

- **Time Complexity:** $\mathcal{O}(N \cdot M)$  
  The entry loop reads through all $N$ data rows sequentially. Splitting or casting strings to numerical types scales with character length $M$. Key insertions, lookups, and scalar mathematical additions inside tracking dictionaries (`word_count`, `speaking_time`, etc.) operate at an average complexity of $\mathcal{O}(1)$.
- **Space Complexity:** $\mathcal{O}(S)$  
  The data structure registers exactly five independent tracking dictionaries, all strictly bounded by the count of unique meeting participants $S$.

#### Ranking & Report Generation

- **Time Complexity:** $\mathcal{O}(S^2)$  
  _where $S$ is the count of unique meeting participants._ \* Locating standard extrema values (e.g., maximum words, minimum words, most questions asked) utilizes simple single-pass loops traversing at $\mathcal{O}(S)$ time.
  - Generating the **Top 5 Speakers by Time** ranking converts the dictionary into an array and runs a nested **Bubble Sort** implementation. This establishes a mathematical worst-case processing footprint of $\mathcal{O}(S^2)$. _(Note: While quadratically inefficient for massive scales, $S$ remains extremely small for business meetings, optimizing practical execution)._
- **Space Complexity:** $\mathcal{O}(S)$  
  Required to instantiate the localized list of tuples (`speaking_time_list`) derived from the primary metrics dictionary to facilitate the inline sorting sequence.

---

### Summary Matrix

| Script / Process             | Time Complexity                             | Space Complexity                     | Primary Resource Driver                                                          |
| :--------------------------- | :------------------------------------------ | :----------------------------------- | :------------------------------------------------------------------------------- |
| **`correct_all_text`**       | $\mathcal{O}(N \cdot M)$                    | $\mathcal{O}(N \cdot M)$             | Prompt compilation payload and API token stream buffering.                       |
| **`feature_enrichement`**    | $\mathcal{O}(N \cdot M)$                    | $\mathcal{O}(S)$                     | Linear row stream tokenization; speaker tracker dictionary scaling.              |
| **`csv_validation`**         | $\mathcal{O}(N)$                            | $\mathcal{O}(E)$ or $\mathcal{O}(1)$ | Single-pass file scanning; error logs compilation.                               |
| **`analytics_stats_output`** | $\mathcal{O}(N \cdot M) + \mathcal{O}(S^2)$ | $\mathcal{O}(S)$                     | Linear dataset reduction followed by a quadratic Bubble Sort on unique speakers. |

- **$N$** = Total number of rows in the CSV file
- **$M$** = Average character length of speaker transcripts
- **$S$** = Number of unique speakers present in the meeting
- **$E$** = Total number of logged dataset validation errors
