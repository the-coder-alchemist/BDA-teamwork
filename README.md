# Team Pipeline Project: Meeting Speech Analytics with Vosk + AI

---

## 1. Project Overview

This repository contains a data analytics pipeline designed for team meeting speech processing. The application records microphone audio during real-time conversations, streams transcription tasks through an open-source speech-to-text model (Vosk), cleans the resulting transcript via an LLM (Gemini), calculates statistics with native Python for each speaker, validates the dataset against a schema, and prints a finalised analytics report.

The architecture is designed so that any user with basic Python and GitHub knowledge can clone this repository, install the required libraries, record their own meeting, and produce a validated, enriched CSV together with a summary report.

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

### Core Concepts

- **Python** — the programming language used throughout the project.
- **Terminal / shell** — a text-based interface for executing commands. On macOS this is typically Terminal.app (running zsh); on Windows it is PowerShell, CMD, or the integrated terminal in VS Code.
- **`cd`** — change directory (move into another folder). The command is identical across platforms.
- **`pwd` / `Get-Location`** — display the current folder path.
- **Virtual environment (`.venv`)** — an isolated Python installation for a specific project. Prevents one project's dependencies from interfering with another's installed packages.
- **`pip`** — Python's package manager. Installs the libraries listed in `requirements.txt`.
- **`requirements.txt`** — the list of Python packages this project depends on. Any user can recreate the same environment with `pip install -r requirements.txt`.
- **README.md** — this file. Markdown syntax reference: <https://www.markdownguide.org/basic-syntax/>.

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

## 6. Create and Activate a Virtual Environment

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

## 7. Install Dependencies

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

## 8. Pipeline Execution Steps

The pipeline operates in five stages.

### Stage 1 and 2: Record and Correct (`gemini_vosk.py`)

Records each speaker turn from the microphone, transcribes it offline with Vosk, then submits every raw transcript to Gemini in a single batch for spelling, punctuation, and casing correction.

> [!NOTE]
> This implementation requires the person running the code to start the recording via the console.

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

## 9. Files Produced

| File                            | Produced by                                    | Purpose                              |
| ------------------------------- | ---------------------------------------------- | ------------------------------------ |
| `group_transcript.csv`          | `gemini_vosk.py` (after renaming `OUTPUT_CSV`) | Raw and Gemini-corrected transcripts |
| `group_transcript_enriched.csv` | `feature_enrichement.py`                       | Adds the five derived columns        |
| Console report                  | `csv_validation.py`                            | Pass or fail summary                 |
| Console report                  | `analytics_stats_output.py`                    | Per-speaker meeting analytics        |

---

## 9. Complexity Discussion

The following tables show complexity estimations generated directly from the `complexity_report_generator.py` of the **Team Pipeline** source code.

### 9.1. Parameter Legend for Analytical Bounds

- $T$: Physical runtime duration of active audio recording streams.
- $N$: Total row records processed inside the pipeline log sheets ($N = 30$ baseline lines).
- $M$: Text statement sizes matching the maximum length of characters per conversational row block.
- $S$: Quantifiable counts of distinct speaking team members tracked in internal lookups ($S \le N$; for Team Pipeline, $S = 6$).

### 9.2. Component Master Metrics Matrix

| Target Source File          | Function Signatures Detected                                                                       | Max Loop Depth | Estimated Time Complexity | Estimated Space Complexity | Core Structural Purpose                                                                            |
| :-------------------------- | :------------------------------------------------------------------------------------------------- | :------------: | :-----------------------: | :------------------------: | :------------------------------------------------------------------------------------------------- |
| `gemini_vosk.py`            | `correct_all_text`, `realtime_transcription`, `save_to_csv`, `main`                                |       2        |    $O(T + N \cdot M)$     |       $O(N \cdot M)$       | Audio streaming capture loop, thread-safe queue handling, and batch cloud LLM semantic formatting. |
| `feature_enrichement.py`    | _(Global Script Block Layout)_                                                                     |       1        |      $O(N \cdot M)$       |           $O(S)$           | Streaming row-by-row structural string inspections and historical participant counts tracking.     |
| `csv_validation.py`         | `validate_timestamp`, `validate_numeric_positive`, `validate_boolean`, `validate_csv_file`, `main` |       1        |          $O(N)$           |           $O(1)$           | Validation bounds check, boundary constraint enforcement, and strict schema validation scanning.   |
| `analytics_stats_output.py` | `analyze_meeting_data`, `main`                                                                     |       2        |   $O(N \cdot M + S^2)$    |           $O(S)$           | Aggregated dictionary accumulation loops and unique speaker tracking via a custom Bubble Sort.     |

---

### 9.3. Comprehensive Function-Level Profiling Breakdown

| Source File Component           | Block Name / Scope Type     | Nested Loop Depth | Est. Time Complexity | Est. Space Complexity | Structural Elements Detected (AST Nodes)                               |
| :------------------------------ | :-------------------------- | :---------------: | :------------------: | :-------------------: | :--------------------------------------------------------------------- |
| **`gemini_vosk.py`**            | `correct_all_text`          |         0         |    $O(N \cdot M)$    |    $O(N \cdot M)$     | 1 x API Client Call, 1 x List Comprehension Join                       |
|                                 | `realtime_transcription`    |         1         |        $O(T)$        |        $O(M)$         | 1 x Threaded Queue Loop, 1 x Active Input Audio Stream                 |
|                                 | `save_to_csv`               |         0         |        $O(1)$        |        $O(1)$         | 1 x File IO context wrapper, 1 x CSV DictWriter row flush              |
|                                 | `main`                      |         1         |        $O(N)$        |    $O(N \cdot M)$     | 1 x Interactive text command menu loop, 1 x Pandas IO sync             |
| **`feature_enrichement.py`**    | `global_stream`             |         1         |    $O(N \cdot M)$    |        $O(S)$         | 1 x Row Iterator, 3 x String Inspectors, 1 x Accumulator Map           |
| **`csv_validation.py`**         | `validate_timestamp`        |         0         |        $O(1)$        |        $O(1)$         | 1 x Try-Except handler, 1 x Datetime Isoformat verification            |
|                                 | `validate_numeric_positive` |         0         |        $O(1)$        |        $O(1)$         | 1 x Conditional Type check, 1 x Positive value comparison              |
|                                 | `validate_boolean`          |         0         |        $O(1)$        |        $O(1)$         | 1 x Primitive Type verification, 1 x Explicit upper string token parse |
|                                 | `validate_csv_file`         |         1         |        $O(N)$        |        $O(1)$         | 1 x Sequenced file reader loop, 6 x Inline checker routing             |
|                                 | `main`                      |         0         |        $O(1)$        |        $O(1)$         | 1 x File path string routing, 1 x Executable runner redirect           |
| **`analytics_stats_output.py`** | `analyze_meeting_data`      |         2         | $O(N \cdot M + S^2)$ |        $O(S)$         | 1 x Read loop, 1 x Custom nested loop Bubble Sort ( $O(S^2)$ )         |
|                                 | `main`                      |         0         |        $O(1)$        |        $O(1)$         | 1 x Production path argument setup, 1 x Analysis suite trigger         |

---
