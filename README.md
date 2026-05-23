# Team Pipeline Project: Meeting Speech Analytics with Vosk + AI

## Team Composition & Functional Role Matrix

The work for this project was systematically divided among members of **Team Pipeline** into specialized functional pairings according to our formal project plan matrix. Each team managed complementary technical areas of the end-to-end data pipeline:

### 1. Sub-Team Allocations & Core Responsibilities

| Role                   | Team Members                      | Core Technical Responsibilities                                                                                                                                   |
| :--------------------- | :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data Engineers**     | Toby Lock<br>William Mckenna      | Local environment configuration, Vosk model installation, audio recording management, and raw CSV stream output initialization.                                   |
| **AI & Logic Devs**    | Carys Williams<br>Mei Len Vorkel  | Gemini API schema integration, batch transcript parsing, correction mapping algorithms, and custom programmatic feature enrichment.                               |
| **QA & Documentation** | Gary Murphy<br>Samuel Weldemariam | File structural integrity checks, boundary value criteria verification, conversational data analytics reporting, Big O reporting, and video presentation editing. |

## 1. Project Overview

This repository contains a data analytics pipeline designed for team meeting speech processing. The application records microphone audio data during real-time conversations, streams transcription tasks using an open-source speech-to-text model, cleans spelling errors via LLM (Large Language Model) API integration, calculates downstream speaking behaviour statistics with native Python routines, validates schema bounds, and prints finalised executive performance summaries.

The architecture ensures that teams can seamlessly clone this repository, install required libraries, and record, validate, and extract conversational intelligence.

---

## 2. Pipeline Execution Steps

Our team implemented the distinct algorithmic pipeline stages outlined below:

### Stage 1 & 2: Record, Transcribe, and AI-Correct (`gemini_vosk.py`)

- **Transcription Strategy:** Uses the `sounddevice` package to read raw mono audio input frames inside an asynchronous queue buffer stream.
- **Local Acoustic Engine:** Feeds buffers blockwise into the `vosk.KaldiRecognizer` machine (`vosk-model-en-us-0.22-lgraph`), aggregating fragmented JSON chunks into a unified `raw_text_vosk` log string.
- **AI Semantic Alignment:** Groups strings systematically and dispatches batch-indexed correction arrays to `gemini-2.5-flash-lite` through the `google-genai` client. A structured prompt ensures the model injects punctuation, fixes syntax gaps, fixes capitalization variations, and matches raw indices without changing semantic context. The results are written back to an intermediate file (`group_transcript.csv`). The OUTPUT_CSV variable in this python file currently writes to a test CSV file (`test_transcript.csv`) to prevent anyone from accidentally overwriting the group transcript CSV file. Change this variable's value in the cloned or forked repository to output to (`group_transcript.csv`) for the subsequent code to work.

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

### Meeting Analytics Pipeline Test Suite

This automated test suite provides regression testing and pipeline integrity checks for the conversational data processing pipeline. It utilizes virtualized in-memory file routing (`io.StringIO`) and function mocking (`unittest.mock.patch`) to evaluate file structural constraints, edge-case mathematical data updates, and report generation accuracy without modifying production data files.

#### Monitored Modules & Files Under Test

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

#### Execution Outputs

Rather than outputting standard terminal dot markers (`...`), the system intercepts test outcomes via a custom `PipelineTestRunner`. Upon execution completion, it overrides normal output streams to cleanly frame a console-based **Pipeline Integrity & Analytics Report**, detailing every individual test function name, its specific architectural file target, and the final verification verdict (`PASS` or `FAIL`).

---

## 3. Algorithmic Space and Time Complexity Analysis

To verify that the Team Pipeline software architecture operates efficiently under scaling workloads, this section provides an algorithmic profiling of our four core engine components.

For the purposes of this analysis:

- $N$ represents the total number of dialogue turn records processed through the pipeline (for our production baseline run, $N = 30$ turns).
- $M$ represents the maximum length of characters or word sequences contained within a single conversational turn.
- $U$ represents the number of unique speaking participants interacting in the meeting transcript ($U \le N$; for Team Pipeline, $U = 6$ core members: _Gary, Carys, William, Samuel, Mei Len, and Toby_).

---

### 4.0 Architectural Efficiency Assessment

| Pipeline Component           | Script Name                 | Time Complexity                 | Space Complexity          | Scaling Behavior Analysis                                                                                                      |
| :--------------------------- | :-------------------------- | :------------------------------ | :------------------------ | :----------------------------------------------------------------------------------------------------------------------------- |
| **1. Audio & AI Capture**    | `gemini_vosk.py`            | $\mathcal{O}(T + N \times M)$   | $\mathcal{O}(N \times M)$ | Scales linearly with recording length and transcription volume. Bound by network API speeds.                                   |
| **2. Feature Enrichment**    | `feature_enrichement.py`    | $\mathcal{O}(N \times M)$       | $\mathcal{O}(U)$          | Fast, stream-based processing layout. Memory stays low even when row counts scale upward.                                      |
| **3. Schema Validation**     | `csv_validation.py`         | $\mathcal{O}(N)$                | $\mathcal{O}(1)$          | Highly efficient baseline scan. Constant memory footprint makes it ideal for large files.                                      |
| **4. Performance Analytics** | `analytics_stats_output.py` | $\mathcal{O}(N \times M + U^2)$ | $\mathcal{O}(U)$          | Runtime is driven by data volume ($N$). The $\mathcal{O}(U^2)$ sorting step remains fast because team sizes are small ($U=6$). |

### 5. Workspace setup

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

### 6. Check Python installation

Check that Python is installed:

```bash
python3 --version
```

On Windows, you can also run:

```powershell (or CMD)
python3 --version
```

### 7. Basics you should know

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

### 8. Create and manage a virtual environment

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

#### 6. Install dependencies

Activate `.venv` again and install dependencies:

```bash
pip install -r requirements.txt
```

If `pip` is missing, run:

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
```

Check the output to ensure everything installed successfully. You can ignore most warnings for the moment.
You are now ready to proceed. You can use the `clear` command to clear the terminal (Windows CMD = cls). Try it out.
