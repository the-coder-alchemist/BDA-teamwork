# Software Pipeline Complexity Analysis Report

This document provides a comprehensive Big-O asymptotic analysis of the core Python modules within the data processing pipeline. It evaluates the **Time Complexity** and **Space Complexity** of individual structural scopes, identifying algorithmic bottlenecks and data scaling thresholds.

---

## Executive Summary Table

| Source File | Scope / Function | Time Complexity | Space Complexity | Dominant Operations & Notes |
| :--- | :--- | :--- | :--- | :--- |
| **`gemini_vosk.py`** | `correct_all_text` | $O(N)$ | $O(N)$ | **Time Complexity:** Scales linearly with text size during string joining and API request construction. <br>**Space Complexity:** Linear overhead required to temporarily hold the batched prompt payload in memory. |
| | `realtime_transcription` | Unbounded / $O(T)$ | $O(T)$ | **Time Complexity:** Event-driven polling loop constrained by real-time recording length. <br>**Space Complexity:** Grows continuously to store raw stream bytes inside the thread-safe processing queue and string buffers. |
| | `save_to_csv` | $O(1)$ | $O(1)$ | **Time Complexity:** Fixed, constant time to perform an isolated disk append operation. <br>**Space Complexity:** Zero persistent allocation beyond transient single-row buffers. |
| | `main` | Unbounded / $O(N)$ | $O(N)$ | **Time Complexity:** Encloses an open-ended interactive console prompt. The batch phase scales linearly to parse transcripts via Pandas. <br>**Space Complexity:** Constrained by reading the entire dataset into memory as a unified DataFrame. |
| **`feature_enrichement.py`** | Row Processing Loop | $O(N \times W)$ | $O(U)$ | **Time Complexity:** Iterates across $N$ total rows while executing string splitting operations that scale with the word length $W$. <br>**Space Complexity:** Efficient row-by-row streaming maintains a flat memory profile, allocating space only for unique speaker IDs ($U$) inside a tracker map. |
| **`csv_validation.py`** | `validate_timestamp` | $O(1)$ | $O(1)$ | **Time Complexity:** Constant lookup runtime utilizing native ISO parsing subroutines. <br>**Space Complexity:** No dynamic variable growth or structure scaling. |
| | `validate_numeric_positive` | $O(1)$ | $O(1)$ | **Time Complexity:** Constant time validation involving basic numeric data conversions and conditional inequality evaluations. <br>**Space Complexity:** Allocation stays completely static. |
| | `validate_boolean` | $O(1)$ | $O(1)$ | **Time Complexity:** Constant time comparison executing membership validations against static array constants. <br>**Space Complexity:** Zero structural memory growth. |
| | `validate_csv_file` | $O(N)$ | $O(E)$ | **Time Complexity:** Evaluates the entire target spreadsheet sequentially, spending uniform constant time across 6 validation rules per line. <br>**Space Complexity:** Allocates list nodes dynamically, scaling exclusively with the total count of reported validation errors ($E$). |
| | `main` | $O(N)$ | $O(E)$ | **Time Complexity:** Directly corresponds to the execution length of the primary `validate_csv_file` pipeline. <br>**Space Complexity:** Memory is governed entirely by the size of the accumulated error trace collection. |
| **`analytics_stats_output.py`** | `analyze_meeting_data` | $O(N + U^2)$ | $O(U)$ | **Time Complexity:** Iterates over $N$ records to update global aggregations. Post-processing triggers an $O(U^2)$ Bubble Sort relative to the count of unique speakers. <br>**Space Complexity:** Maintains 5 decoupled dictionaries that scale linearly with the unique speaker count ($U$). |
| | `main` | $O(N + U^2)$ | $O(U)$ | **Time Complexity:** Replicates the combined row aggregation and nested Bubble Sort execution paths. <br>**Space Complexity:** Constrained exclusively by data structures storing tracking records for distinct speakers. |

*Notation Key:*
- $N$: Total number of transcript rows, utterances, or text records processed.
- $W$: Average word count per individual text line.
- $T$: Continuous execution duration of real-time audio capturing.
- $U$: Count of unique, distinct speakers detected in the dataset ($U \le N$).
- $E$: Total volume of discrete validation errors caught during processing.

---

## Detailed Architectural Analysis

### 1. Audio Processing & Synthesis (`gemini_vosk.py`)
- **Algorithmic Overview:** Combines live offline audio streaming with cloud-based batch processing model execution.
- **Time Complexity Bottlenecks:** The live capturing loop is inherently unbounded since it hooks directly into continuous peripheral hardware audio. The optimization to bundle transcripts into a single numbered array before issuing the `genai.Client` call dramatically reduces network handshaking delays from $O(N)$ API trips down to a single $O(1)$ batched call.
- **Space Complexity Drivers:** Audio data packets are pulled dynamically and held inside a thread-safe memory queue (`queue.Queue()`). Long-running records will exhibit continuous, monotonic memory accumulation until the stream is flushed.

### 2. Metric Enrichment Pipeline (`feature_enrichement.py`)
- **Algorithmic Overview:** Extends raw transcript files with analytical parameters (word metrics, frequency rates, and conditional markers).
- **Time Complexity Bottlenecks:** Row computation takes $O(W)$ time due to standard string tokenization (`.split()`) occurring over every single text line.
- **Space Complexity Drivers:** Highly optimized design pattern. By utilizing streaming handlers (`csv.DictReader` and `csv.DictWriter`) instead of in-memory caching layers, raw file contents pass through a single element window. Persistent memory footprints scale exclusively with tracking states ($counter$) for unique speaker identities ($U$).

### 3. Data Integrity & Verification (`csv_validation.py`)
- **Algorithmic Overview:** A structural syntax gate checking for data format correctness, types, boundaries, and timestamps.
- **Time Complexity Bottlenecks:** Runs a flat data iteration routine, verifying each item against independent validator functions that possess guaranteed $O(1)$ execution guarantees. Total execution maps directly onto file length.
- **Space Complexity Drivers:** In ideal run conditions where data passes validation checks perfectly, memory space defaults to a pristine $O(1)$. It scales to $O(E)$ only to collect context traces for broken lines.

### 4. Downstream Metric Aggregation (`analytics_stats_output.py`)
- **Algorithmic Overview:** Synthesizes file outputs to output global presentation layers, leaderboards, and rate evaluations.
- **Time Complexity Bottlenecks:** Incorporates a nested **Bubble Sort** routine to organize speaker times. While sorting lists under standard enterprise datasets typically mandates $O(U \log U)$ paradigms, this script runs an $O(U^2)$ comparison architecture. This design remains highly acceptable since the total unique speaker variable ($U$) in human meetings is naturally restricted.
- **Space Complexity Drivers:** Keeps file parsing steps decoupled across 5 granular key-value mapping structures, safely isolating records to track independent features per speaker.
