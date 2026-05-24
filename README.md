# Team Pipeline Project: Meeting Speech Analytics with Vosk + AI

---

## 1. Project Overview

This repository contains a data analytics pipeline designed for team meeting speech processing. The application records microphone audio during real-time conversations, streams transcription tasks through an open-source speech-to-text model (Vosk), cleans the resulting transcript via an LLM (Gemini), calculates per-speaker speaking-behaviour statistics with native Python, validates the dataset against a schema, and prints a finalised analytics report.

The architecture is designed so that any user can clone this repository, install the required libraries, record their own meeting, and produce a validated, enriched CSV together with a summary report.

---

## 2. Cross-Platform Shell Quick Reference

Before proceeding, this section provides a reference table for translating commands between operating systems and shells. Throughout this README, commands are shown for **macOS / Linux** (`bash` or `zsh`) and for **Windows** (`PowerShell` and `Command Prompt / CMD`). Shell differences are a more frequent source of difficulty than the Python code itself, so reviewing this section once is recommended.

| Task                          | macOS / Linux (bash, zsh)                     | Windows PowerShell                            | Windows Command Prompt (CMD) |
| ----------------------------- | --------------------------------------------- | --------------------------------------------- | ---------------------------- |
| Show current folder           | `pwd`                                         | `Get-Location` or `pwd`                       | `cd` (no argument)           |
| List files                    | `ls`                                          | `Get-ChildItem` or `ls`                       | `dir`                        |
| Change folder                 | `cd path/to/folder`                           | `cd path\to\folder`                           | `cd path\to\folder`          |
| Go up one folder              | `cd ..`                                       | `cd ..`                                       | `cd ..`                      |
| Clear the screen              | `clear`                                       | `Clear-Host` or `cls`                         | `cls`                        |
| Path separator                | `/` (forward slash)                           | `\` (backslash; `/` is also usually accepted) | `\` (backslash)              |
| Run Python                    | `python3`                                     | `python` or `py`                              | `python` or `py`             |
| Set env variable (session)    | `export VAR="value"`                          | `$env:VAR="value"`                            | `set VAR=value`              |
| Set env variable (persistent) | Add `export ...` to `~/.zshrc` or `~/.bashrc` | `[Environment]::SetEnvironmentVariable(...)`  | `setx VAR "value"`           |
| Read env variable             | `echo $VAR`                                   | `echo $env:VAR`                               | `echo %VAR%`                 |
| Activate `.venv`              | `source .venv/bin/activate`                   | `.venv\Scripts\Activate.ps1`                  | `.venv\Scripts\activate.bat` |
| Deactivate `.venv`            | `deactivate`                                  | `deactivate`                                  | `deactivate`                 |
| Delete a file                 | `rm file.csv`                                 | `Remove-Item file.csv` or `del file.csv`      | `del file.csv`               |
| Delete a folder               | `rm -r folder/`                               | `Remove-Item -Recurse folder`                 | `rmdir /s folder`            |

### Common pitfalls

**bash versus zsh on macOS.** macOS has used `zsh` as the default shell since macOS Catalina (2019). The majority of commands in this README operate identically in both shells, but if external documentation references `~/.bashrc`, the zsh equivalent on a modern macOS installation is `~/.zshrc`.

**`python` versus `python3` versus `py`.** On most macOS and Linux installations, `python` is either missing or refers to Python 2; the correct command is `python3`. On Windows the launcher is usually `py`, which automatically selects the most recent installed Python 3. If a command in this README fails because the interpreter is not found, substitute `python3`, `python`, or `py` and retry.

**PowerShell execution policy.** If `.venv\Scripts\Activate.ps1` is rejected with an error indicating _"running scripts is disabled on this system"_, run PowerShell as Administrator once and execute:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then reopen the terminal and retry the activation. As an alternative that does not require a policy change, invoke the venv's Python directly: `.venv\Scripts\python.exe your_script.py`.

**Quotation handling in environment variables.** PowerShell and bash both accept `"PASTE_YOUR_KEY"` as a quoted value, but **CMD's `set` command stores the surrounding quotation marks as part of the value**. On CMD, use `set GEMINI_API_KEY=PASTE_YOUR_KEY` (without quotes). On PowerShell and bash, the quotes are correct.

**Line endings.** macOS and Linux use `\n` (line feed); Windows uses `\r\n` (carriage return followed by line feed). Python's `csv` module with the `newline=''` argument handles both conventions automatically, and the code in this repository already does so. If a CSV opened in a text editor shows `^M` at the end of every line, the file is in Windows format viewed on a Unix system.

---

## 3. Workspace Setup

1. Install **Git** if it is not already installed.
   - **macOS:** `brew install git` (requires [Homebrew](https://brew.sh/)), or download from [git-scm.com](https://git-scm.com/).
   - **Linux:** `sudo apt install git` (Debian/Ubuntu), `sudo dnf install git` (Fedora), or the equivalent for the distribution in use.
   - **Windows:** download and run the installer from [git-scm.com](https://git-scm.com/download/win). The installer also provides "Git Bash", a bash-like terminal that is often more convenient than CMD.
2. Install [Visual Studio Code](https://code.visualstudio.com/), or any preferred editor. If VS Code was already open when Git was installed, restart it so that the updated PATH is loaded.
3. Open a terminal.
4. Clone the repository:

   ```bash
   git clone https://github.com/the-coder-alchemist/BDA-teamwork.git
   ```

   > [!TIP]
   > If the repository already exists locally, run `git pull` from inside the folder rather than cloning again.

5. Open the project folder in VS Code (`File > Open Folder...`).
6. Open a terminal inside VS Code: `Terminal > New Terminal`. VS Code uses the system default shell unless an alternative is selected (`Ctrl+Shift+P` → "Terminal: Select Default Profile").
7. Use `cd` to navigate into the project folder if it is not already the active directory.

---

## 4. Check Python Installation

```bash
# macOS / Linux
python3 --version
```

```powershell
# Windows PowerShell or CMD
python --version
# or
py --version
```

Python 3.10 or newer is required for this project. If the command is not found, install Python from [python.org](https://www.python.org/downloads/). On Windows, ensure the option _"Add Python to PATH"_ is selected during installation.

---

## 5. Create the Gemini API Key (free tier)

1. Navigate to Google AI Studio: <https://aistudio.google.com/app/api-keys>
2. Sign in with a Gmail account.
3. Select **Create API key**, provide a name (or accept the default), and choose `Default Gemini Project`.
4. Copy the key (it begins with `AIza...`). Treat the key as confidential, similar to a password.

### Setting the key in the terminal

**macOS / Linux (bash or zsh):**

```bash
export GEMINI_API_KEY="PASTE_YOUR_KEY"
```

To make the value persist across new terminals, add the same line to `~/.zshrc` (modern macOS) or `~/.bashrc` (most Linux distributions), then either restart the terminal or run `source ~/.zshrc`.

**Windows PowerShell (session-only):**

```powershell
$env:GEMINI_API_KEY="PASTE_YOUR_KEY"
```

**Windows PowerShell (persistent across sessions):**

```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "PASTE_YOUR_KEY", "User")
```

Restart VS Code, or open a new terminal, for the change to take effect.

**Windows Command Prompt (session-only):**

```cmd
set GEMINI_API_KEY=PASTE_YOUR_KEY
```

Note: do **not** enclose the value in quotation marks when using `set`. CMD treats the quotes as part of the stored value.

**Windows Command Prompt (persistent):**

```cmd
setx GEMINI_API_KEY "PASTE_YOUR_KEY"
```

Restart VS Code, or open a new terminal, for `setx` to apply.

> [!TIP]
> The code in `gemini_vosk.py` batches every raw transcript into a single Gemini call to remain within the free-tier quota. To use OpenAI instead, replace `os.environ["GEMINI_API_KEY"]` with `os.environ["OPENAI_API_KEY"]` and update the client construction accordingly.

### Verify that the key is set

```bash
# macOS / Linux / Git Bash
python3 -c 'import os; k=os.getenv("GEMINI_API_KEY"); print("Set:", bool(k), "Length:", len(k) if k else 0)'
```

```powershell
# Windows PowerShell / CMD
python -c "import os; k=os.getenv('GEMINI_API_KEY'); print('Set:', bool(k), 'Length:', len(k) if k else 0)"
```

If the output indicates `Set: True` and a non-zero length, the configuration is complete.

> [!TIP]
> Google AI Studio is free of charge but rate-limited (typically 5–15 requests per minute, depending on model and tier). Current quotas are documented at <https://ai.google.dev/gemini-api/docs/quota>. Exceeding the limit returns HTTP status code `429` until the quota resets.

---

## 6. Core Concepts

- **Python** — the programming language used throughout the project.
- **Terminal / shell** — a text-based interface for executing commands. On macOS this is typically Terminal.app (running zsh); on Windows it is PowerShell, CMD, or the integrated terminal in VS Code.
- **`cd`** — change directory (move into another folder). The command is identical across platforms.
- **`pwd` / `Get-Location`** — display the current folder path.
- **Virtual environment (`.venv`)** — an isolated Python installation for a specific project. Prevents one project's dependencies from interfering with another's installed packages.
- **`pip`** — Python's package manager. Installs the libraries listed in `requirements.txt`.
- **`requirements.txt`** — the list of Python packages this project depends on. Any user can recreate the same environment with `pip install -r requirements.txt`.
- **README.md** — this file. Markdown syntax reference: <https://www.markdownguide.org/basic-syntax/>.

---

## 7. Create and Activate a Virtual Environment

> [!TIP]
> Ensure the working directory is the project folder (`cd BDA-teamwork`) before creating the virtual environment.

**Create the virtual environment:**

```bash
# macOS / Linux
python3 -m venv .venv
```

```powershell
# Windows
python -m venv .venv
# or, if 'python' is missing:
py -m venv .venv
```

The leading dot in `.venv` causes the folder to be hidden on Unix-style filesystems. On Windows, the folder is treated as standard.

**Activate the virtual environment:**

| Shell                     | Activation command              |
| ------------------------- | ------------------------------- |
| bash / zsh (macOS, Linux) | `source .venv/bin/activate`     |
| Git Bash on Windows       | `source .venv/Scripts/activate` |
| PowerShell                | `.venv\Scripts\Activate.ps1`    |
| Command Prompt (CMD)      | `.venv\Scripts\activate.bat`    |

The prompt should now begin with `(.venv)`. If PowerShell rejects the activation script, refer to the _"PowerShell execution policy"_ entry in section 2.

**Deactivate when finished:**

```bash
deactivate
```

This command operates identically across every shell.

---

## 8. Install Dependencies

With `.venv` activated:

```bash
pip install -r requirements.txt
```

If `pip` itself is unavailable (uncommon but possible):

```bash
# macOS / Linux
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
```

```powershell
# Windows
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

The `requirements.txt` file pins the exact versions used during development:

```text
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

Specifying exact version numbers—known as 'pinning'—ensures your project always uses the exact same code, i.e. improves reproducibility, preventing unexpected bugs when external libraries change. The trade-off is that you must manually update these pinned versions to get the latest security fixes and improvements when upstream libraries release patches.

### Vosk model download

Download `vosk-model-en-us-0.22-lgraph` (128 MB) from <https://alphacephei.com/vosk/models> and unzip it into the project root. The resulting structure should be:

```text
BDA-teamwork/
├── gemini_vosk.py
├── vosk-model-en-us-0.22-lgraph/
│   ├── am/
│   ├── conf/
│   ├── graph/
│   └── ...
```

---

## 9. Pipeline Execution Steps

The pipeline operates in five stages.

### Stage 1 and 2: Record and Correct (`gemini_vosk.py`)

Records each speaker turn from the microphone, transcribes it offline with Vosk, then submits every raw transcript to Gemini in a single batch for spelling, punctuation, and casing correction.

```bash
python gemini_vosk.py
```

At the prompt, press **R** to record a new utterance (the speaker's name is requested first, after which `Ctrl+C` stops the recording) or **Q** to finish and trigger Gemini cleanup. Output is written to `test_transcript.csv` by default; rename the `OUTPUT_CSV` constant to `group_transcript.csv` before the final run so that the downstream stages can locate the file.

Example raw row:

| timestamp                    | name            | raw_text_vosk                                                                                          | time_taken_sec |
| ---------------------------- | --------------- | ------------------------------------------------------------------------------------------------------ | -------------- |
| `2026-05-10T12:59:12.495072` | Carys Williams  | `i've been tracking use a sign ups and while they're up the conversion from free to pay is low`        | `8.26`         |
| `2026-05-10T12:59:27.960636` | William McKenna | `i think the onboarding flow is the bottle neck is currently taking users too long to find the valley` | `10.07`        |
| `2026-05-10T12:59:42.62123`  | Gary Murphy     | `that's a fair points caris what does the pricing feedback look like from those early users`           | `8.1`          |

Example after Gemini correction:

| timestamp                    | name               | raw_text_vosk                                                                                      | text                                                                                                   | time_taken_sec |
| ---------------------------- | ------------------ | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------- |
| `2026-05-10T13:01:15.176884` | Toby Lock          | `of allocated budget for the security audit but we need to decide if we're hiring more developers` | `I've allocated budget for the security audit, but we need to decide if we're hiring more developers.` | `9.24`         |
| `2026-05-10T13:01:44.795188` | Mei Len Vorkel     | `we definitely need of back and specialist if we plan on horizontal scaling by careful`            | `We definitely need a backend specialist if we plan on horizontal scaling. But be careful`             | `8.33`         |
| `2026-05-10T13:02:07.814951` | Samuel Weldemariam | `if we hire know i can start building the brand story around on new speed and security focus`      | `If we hire now, I can start building the brand story around our new speed and security focus`         | `8.96`         |

### Stage 3: Enrich (`feature_enrichement.py`)

Adds five derived columns to the raw CSV using pure Python (no AI involvement). Reads from `group_transcript.csv` and writes `group_transcript_enriched.csv`.

```bash
python feature_enrichement.py
```

| Column              | Calculation                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| `has_question_mark` | `True` if `text` contains `?`, otherwise `False`                                               |
| `num_words_in_text` | Whitespace-split word count of `text`                                                          |
| `text_size_chars`   | Character length of `text`                                                                     |
| `speech_rate_wps`   | `num_words_in_text / time_taken_sec`, rounded to 2 decimal places                              |
| `speaker_counter`   | Running count of this speaker's utterances (1 for the first turn, 2 for the second, and so on) |

> [!NOTE]
> The assignment brief specifies slightly different column names (`question_flag`, `num_words`, `speaker_turn_id`). The implementation uses the names listed above. Validation and analytics both read the implementation names.

### Stage 4: Validate (`csv_validation.py`)

Reads `group_transcript_enriched.csv` and verifies every row:

```bash
python csv_validation.py
```

Validation rules:

- Every `timestamp` value parses as an ISO 8601 datetime.
- `time_taken_sec`, `num_words_in_text`, `speech_rate_wps`, and `speaker_counter` are numeric and strictly greater than zero.
- `has_question_mark` is a boolean (the validator accepts `True` and `False` in any letter case, including the string form).

Failures are reported as follows:

```text
Validation failed:
- Row 4: timestamp "-04-28T10:00:05" is not a valid datetime
- Row 3: speech_rate_wps '0' is not greater than 0
```

A passing run produces:

```text
Validation passed!
All 30 rows are valid.
```

### Stage 5: Analytics (`analytics_stats_output.py`)

Aggregates per-speaker statistics and prints a summary report. The ranking of the top five speakers by total speaking time is produced by a hand-written bubble sort applied to a list of `(speaker, time)` tuples.

```bash
python analytics_stats_output.py
```

Questions answered:

1. Who spoke the most by total words?
2. Who spoke the least by total words?
3. What is the total speaking time of the meeting?
4. What is the average speaking time per speaker?
5. Who asked the most questions?
6. Who are the top 5 speakers by total speaking time?
7. What is each speaker's average speech rate?

Example output:

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
...
==================================================
```

---

## 10. Test Suite (`pipeline_unit_testing.py`)

Automated tests for the pipeline. Uses `unittest`, together with `unittest.mock.patch` and `io.StringIO`, to supply mocked CSV data without writing to disk.

```bash
python pipeline_unit_testing.py
```

The suite includes the following tests:

- **`test_validate_timestamp_formats`** — Confirms that ISO timestamps pass validation and that malformed values fail with an informative message.
- **`test_validate_boolean_formats`** — Confirms that `"TRUE"`, `"false"`, and the native `True` are accepted, and that `"Yes"` is rejected.
- **`test_numeric_positive_boundaries`** — Verifies boundary cases: a positive value passes; `0` and negative values fail (strict greater-than); non-numeric input fails with a distinct error message.
- **`test_feature_enrichment_logic`** — Patches `builtins.open` and verifies that the new columns appear, that `num_words / time_taken_sec` is computed correctly, and that the per-speaker counter increments as expected. Triggers `feature_enrichement` via an `importlib.reload`, since the enrichment runs as a top-level script body rather than inside a callable function.
- **`test_analytics_data_reporting`** — Patches `builtins.open` and `sys.stdout`, runs the analytics function, and asserts that the report contains the expected aggregates in the correct sort order produced by the bubble-sort implementation.

A successful run produces a custom report:

```text
================================================================================
                    PIPELINE INTEGRITY & ANALYTICS REPORT
================================================================================
Total Tests Executed: 5
Successful Passes   : 5
Failures / Crashes  : 0
--------------------------------------------------------------------------------
TEST METHOD NAME                    | TARGET SOURCE FILE        | VERIFICATION VERDICT
--------------------------------------------------------------------------------
test_analytics_data_reporting       | analytics_stats_output.py | PASS (✓)
  └─ Objective: Verify bubble-sorting metrics and text aggregation output.
test_feature_enrichment_logic       | feature_enrichement.py    | PASS (✓)
  └─ Objective: Test feature enrichment equations and row modification.
test_numeric_positive_boundaries    | csv_validation.py         | PASS (✓)
  └─ Objective: Verify numeric boundaries (> 0 constraint).
test_validate_boolean_formats       | csv_validation.py         | PASS (✓)
  └─ Objective: Ensure boolean validations cleanly capture various cases.
test_validate_timestamp_formats     | csv_validation.py         | PASS (✓)
  └─ Objective: Ensure ISO timestamps pass and malformed ones fail.
================================================================================
```

---

## 11. Time and Space Complexity Analysis

This section documents the complexity of every public function in the pipeline as implemented in this repository.

### Notation

| Symbol | Meaning                                                               |
| ------ | --------------------------------------------------------------------- |
| `N`    | Number of rows (utterances) in the CSV                                |
| `S`    | Number of unique speakers (always `S ≤ N`)                            |
| `L`    | Average character length of the `text` field per row                  |
| `E`    | Number of validation errors recorded (worst case `6N`, best case `0`) |
| `T`    | Total duration in seconds of a live audio recording                   |
| `W`    | Total transcribed character count from the live stream                |
| `R`    | Length of the response returned by the Gemini API                     |
| `M`    | Number of recordings made in a single `gemini_vosk.main()` session    |
| `t`    | Number of test methods in the unit-test suite                         |
| `m`    | Number of rows in mocked CSV strings inside tests                     |
| `o`    | Size of captured stdout during a test                                 |
| `P`    | Source-file size of a module being reloaded (`importlib.reload`)      |

### 11.1 Meeting Analytics — `analytics_stats_output.py`

#### `analyze_meeting_data(file_path)`

Aggregates per-speaker statistics from an enriched transcript and prints a report.

- **Time:** `O(N + S²)`.
  - **Streaming pass over the file:** `O(N)`. Each row triggers a constant number of `O(1)` dictionary updates (word totals, question totals, speaking time, speech-rate running totals).
  - **Aggregation across speakers:** `O(S)`. Identifying the most and least words, the most-questions speaker, and the total and average time each requires iterating over the speaker dictionaries.
  - **Sorting:** `O(S²)`. A hand-written nested-loop bubble sort ranks the `(speaker, time)` tuples in descending order so that the top five can be selected.
- **Space:** `O(S)`. The five aggregate dictionaries plus the list of `(speaker, time)` tuples used for sorting all scale with the number of unique speakers. The file itself is streamed rather than loaded into memory.

> **Practical impact:** For typical meetings `S` is small (under twenty speakers), so the quadratic sort is not a runtime concern. The linear file scan `O(N)` dominates the wall-clock cost in practice. A future refactor to `sorted(...)` would reduce the worst case to `O(S log S)` without changing observable output.

### 11.2 CSV Validation — `csv_validation.py`

#### `validate_timestamp(value, field_name, row_num)`

- **Time:** `O(1)`. `datetime.fromisoformat` parses a fixed-format string in constant time.
- **Space:** `O(1)`.

#### `validate_numeric_positive(value, field_name, row_num)`

- **Time:** `O(1)`. One `float()` cast and one comparison.
- **Space:** `O(1)`.

#### `validate_boolean(value, field_name, row_num)`

- **Time:** `O(1)`. Two `isinstance` checks and a membership test against a 2-element list.
- **Space:** `O(1)`.

#### `validate_csv_file(file_path)`

Applies the three helper functions to every row of the enriched CSV.

- **Time:** `O(N)`. Six `O(1)` validations per row, repeated `N` times.
- **Space:** `O(E)`. The `validation_errors` list accumulates at most six entries per row, resulting in `O(1)` space for a clean file and `O(N)` space if every field fails. The file itself is streamed.

### 11.3 Feature Enrichment — `feature_enrichement.py`

#### Main script execution

The enrichment logic runs at module top level rather than inside a callable function; it executes as soon as the module is imported. The block opens both files, iterates through the input rows, derives the five new columns, and writes each enriched row to the output file.

- **Time:** `O(N × L)`. The dominant per-row operations are `'?' in text` and `text.split()`, both of which scan the string in time proportional to its length. When utterances are short, `L` is effectively constant and the complexity reduces to `O(N)`.
- **Space:** `O(S)`. The reader and writer process one row at a time; only the per-speaker `counter` dictionary grows with input size.

### 11.4 Recording and Cleanup — `gemini_vosk.py`

#### `correct_all_text(texts)`

Bundles every raw transcript into a single Gemini API call.

- **Time:** `O(L_total + R)`, where `L_total` is the combined length of all transcripts and `R` is the response length. Local work — constructing the numbered prompt and parsing the response — is linear in the input size. The API round-trip itself is network-bound and is excluded from the algorithmic analysis.
- **Space:** `O(L_total + R)`. The numbered prompt and the response are held in memory concurrently.

#### `realtime_transcription()`

Records from the microphone until `Ctrl+C` is pressed, then returns the joined transcript.

- **Time:** `O(d + L²)` in the worst case, where `d` is the number of audio blocks processed and `L` is the total transcribed length. Each block is processed by Vosk in constant time from the Python side. Text fragments are accumulated using `full_text += text + " "` within the loop. Because Python strings are immutable, each `+=` operation allocates a new string and copies the existing contents, giving quadratic worst-case cost in the total length. In practice the cost is closer to linear for short transcripts due to CPython implementation details, but the asymptotic worst case remains `O(L²)`.
- **Space:** `O(d + L)`. The audio queue holds up to `d` pending blocks; the accumulated `full_text` string contains `L` characters in total.

> **Practical impact:** For meetings consisting of short utterances the quadratic behaviour is rarely observed. For long, uninterrupted recordings, replacing `+=` with a list-and-join pattern would reduce the worst case to `O(L)` without affecting the returned string.

#### `save_to_csv(data)`

Appends a single row to the output CSV.

- **Time:** `O(1)` (assuming a bounded row size).
- **Space:** `O(1)`.

#### `main()`

Drives the record-and-quit loop, then batch-corrects all captured transcripts.

- **Time:** `O(M × T_record + N + L_total)`. The record loop iterates `M` times, each iteration consuming one recording's duration. After the loop, `pd.read_csv` is `O(N)`, `correct_all_text` is `O(L_total)`, splitting the numbered response from Gemini is `O(L_total)`, and `to_csv` is `O(N × k)` for some bounded row size `k`.
- **Space:** `O(N × k)`. Unlike the streaming functions in other modules, this one loads the entire CSV into a Pandas DataFrame. This is the memory bottleneck of the pipeline; for very large transcripts, refactoring to a streaming update would be advisable.

### 11.5 Test Harness — `pipeline_unit_testing.py`

#### `NonClosingStringIO.close()` and `force_close()`

- **Time and Space:** `O(1)` each. The `close()` method intentionally performs no action so that `with` blocks in the code under test cannot discard the buffer; `force_close()` provides the manual cleanup path.

#### `PipelineTestResult.__init__` and `addSuccess(test)`

- **Time:** `O(1)` per call. Recording a success consists of a fixed-size dictionary lookup and a list append.
- **Space:** `O(1)` per call. The `successes` list grows to `O(t)` over the course of a complete run.

#### `TestPipeline` — validator tests

The three csv_validation tests (`test_validate_timestamp_formats`, `test_validate_boolean_formats`, `test_numeric_positive_boundaries`) each execute a small number of `O(1)` calls against fixed input strings.

- **Time:** `O(1)`. **Space:** `O(1)`.

#### `TestPipeline.test_feature_enrichment_logic`

Patches `builtins.open` with two `NonClosingStringIO` buffers, then reloads `feature_enrichement` so that its top-level enrichment code runs against the mocked files.

- **Time:** `O(P + m × L)`. The `importlib.reload` operation incurs a one-time `O(P)` cost to re-parse and re-execute the module's source; the enrichment then runs in `O(m × L)` against the mocked rows.
- **Space:** `O(m × L)`. Both mock buffers retain the CSV content in memory.

#### `TestPipeline.test_analytics_data_reporting`

Patches `builtins.open`, redirects `sys.stdout`, executes `analyze_meeting_data`, and asserts on the captured report.

- **Time:** `O(m + S² + o)`. The analytics function dominates — its `O(S²)` bubble sort is the largest term for any non-trivial speaker count, although for the three-row mocked CSV used in the test it remains effectively constant. The substring `assertIn` checks against the captured output are `O(o)` each.
- **Space:** `O(m × L + o)`. The mocked CSV and the captured stdout buffer are the two primary memory consumers.

### 11.6 Summary Table

| Module                      | Function                        | Time                            | Space             |
| --------------------------- | ------------------------------- | ------------------------------- | ----------------- |
| `analytics_stats_output.py` | `analyze_meeting_data`          | `O(N + S²)`                     | `O(S)`            |
| `csv_validation.py`         | `validate_timestamp`            | `O(1)`                          | `O(1)`            |
| `csv_validation.py`         | `validate_numeric_positive`     | `O(1)`                          | `O(1)`            |
| `csv_validation.py`         | `validate_boolean`              | `O(1)`                          | `O(1)`            |
| `csv_validation.py`         | `validate_csv_file`             | `O(N)`                          | `O(E)`            |
| `feature_enrichement.py`    | Top-level script execution      | `O(N × L)`                      | `O(S)`            |
| `gemini_vosk.py`            | `correct_all_text`              | `O(L_total + R)`                | `O(L_total + R)`  |
| `gemini_vosk.py`            | `realtime_transcription`        | `O(d + L²)` worst case          | `O(d + L)`        |
| `gemini_vosk.py`            | `save_to_csv`                   | `O(1)`                          | `O(1)`            |
| `gemini_vosk.py`            | `main`                          | `O(M × T_record + N + L_total)` | `O(N × k)`        |
| `pipeline_unit_testing.py`  | `NonClosingStringIO.*`          | `O(1)`                          | `O(1)`            |
| `pipeline_unit_testing.py`  | `PipelineTestResult.*`          | `O(1)` per call                 | `O(t)` cumulative |
| `pipeline_unit_testing.py`  | validator tests (each)          | `O(1)`                          | `O(1)`            |
| `pipeline_unit_testing.py`  | `test_feature_enrichment_logic` | `O(P + m × L)`                  | `O(m × L)`        |
| `pipeline_unit_testing.py`  | `test_analytics_data_reporting` | `O(m + S² + o)`                 | `O(m × L + o)`    |

### 11.7 Key Observations

The pipeline is **linear in the number of utterances** for every stage that interacts with the CSV directly. Two implementations contain non-linear cost paths:

1. **Bubble sort in `analyze_meeting_data`** (`O(S²)`). The hand-written nested-loop sort is asymptotically slower than necessary, but `S` is typically below twenty for meeting data so the practical runtime impact is negligible. Substituting Python's built-in `sorted(...)` would reduce the cost to `O(S log S)`.
2. **String concatenation in `realtime_transcription`** (`O(L²)` worst case). The use of `full_text += text + " "` within the recording loop creates quadratic worst-case behaviour due to Python string immutability. For typical recording lengths the cost remains acceptable, but very long recordings would benefit from a list-and-join refactor.

The memory bottleneck is `gemini_vosk.main()`, which loads the entire CSV into a Pandas DataFrame; every other stage processes data row-by-row.

---

## 12. Files Produced

| File                            | Produced by                                    | Purpose                              |
| ------------------------------- | ---------------------------------------------- | ------------------------------------ |
| `group_transcript.csv`          | `gemini_vosk.py` (after renaming `OUTPUT_CSV`) | Raw and Gemini-corrected transcripts |
| `group_transcript_enriched.csv` | `feature_enrichement.py`                       | Adds the five derived columns        |
| Console report                  | `csv_validation.py`                            | Pass or fail summary                 |
| Console report                  | `analytics_stats_output.py`                    | Per-speaker meeting analytics        |
| Console report                  | `pipeline_unit_testing.py`                     | Per-test verdict table               |

---

## 13. Troubleshooting

| Symptom                                       | Likely cause                                                | Resolution                                                                                                                        |
| --------------------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'vosk'` | `.venv` is not activated, or `pip install` has not been run | Activate `.venv` (section 7) and re-run `pip install -r requirements.txt`                                                         |
| `KeyError: 'GEMINI_API_KEY'`                  | Environment variable is not set in the current shell        | Re-run the `export`, `$env:`, or `set` command from section 5. New VS Code terminals do not inherit unsaved environment variables |
| PowerShell refuses to execute `Activate.ps1`  | Execution policy restriction                                | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once, then restart the terminal                        |
| `python: command not found` on macOS or Linux | Only `python3` is installed                                 | Use `python3` instead of `python`, or define an alias `python=python3` in the shell configuration file                            |
| HTTP status `429` returned from Gemini        | Free-tier rate limit exceeded                               | Wait one minute, then retry. Consider increasing the batch size per call                                                          |
| CSV displays incorrectly when opened in Excel | Locale uses `;` as the field separator                      | Use Data → "From Text/CSV" and explicitly select comma                                                                            |
| `OSError: [Errno -9986]` from `sounddevice`   | macOS has not granted microphone permission                 | System Settings → Privacy & Security → Microphone → enable the relevant terminal application or VS Code                           |
