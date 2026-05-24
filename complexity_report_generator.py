from __future__ import annotations

"""
Generate one CSV complexity report per Python file listed in the TARGET_FILES constant. WARNING: Do not attempt to include this file i.e. the complexity report generator, in the TARGET_FILES list. It will result in an infinite loop.

The script attempts to import each target module (best-effort, isolated in a
subprocess so import-time side effects or missing third-party packages do not
stop the report), then uses Python's AST (Abstract Syntax Tree) to estimate time and space complexity
for every top-level function plus module-level code.

Usage:
    python complexity_report_generator.py

Outputs:
    complexity_reports/<source_file_stem>_complexity.csv
"""

"""
# In Python, from __future__ import ... is a special directive that tells the Python interpreter to use a feature that is planned to become the standard default in a later version of the language.
# Specifically, from __future__ import annotations changes how Python handles type hints (type annotations).

The Problem It Solves: Forward References
By default, Python evaluates type hints at runtime when the module is imported. This creates a classic "chicken-and-egg" problem called a forward reference.

If you try to use a class as a type hint inside its own definition or before it has been defined in the file, Python will throw a NameError.
"""

# Metadata
__author__ = []
__credits__ = ["Carys Williams","Gary Murphy", "William McKenna", "Mei Len Vorkel", "Samuel Weldemariam", "Toby Lock"]
__version__ = "1.0.0"

# Custom Academic Attribution Matrix
__team__ = "The Pipeline"
__module__ = "Big Data Analytics (BUCI065H7)"
__assignment__ = "Assignment 1 - Startup Meeting Speech Analytics"



import ast
import csv
import importlib.util
import multiprocessing as mp
import os
from pathlib import Path
import sys
import traceback
from typing import Iterable

# Kept self-analysis out of this list to eliminate any recursion risk
TARGET_FILES = [
    "analytics_stats_output.py",
    "csv_validation.py",
    "feature_enrichement.py",
    "gemini_vosk.py",
    "pipeline_unit_testing.py",
]

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "complexity_reports"

CSV_FIELDS = [
    "source_file",
    "import_status",
    "import_error",
    "scope_type",
    "scope_name",
    "line_start",
    "line_end",
    "time_complexity_estimate",
    "space_complexity_estimate",
    "dominant_operations",
    "confidence",
    "notes",
]


def _import_worker(path_text: str, queue: mp.Queue) -> None:
    """Import a module in a child process and return status through a queue.

    This worker isolates the import execution to protect the main process from 
    import-time side effects, syntax errors, or unhandled exceptions.

    Args:
        path_text: The string file path of the target Python module.
        queue: A multiprocessing Queue used to send the status back to the parent.
    """
    path = Path(path_text)
    module_name = path.stem
    try:
        sys.path.insert(0, str(path.parent))
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not create import spec for {path.name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        queue.put(("success", ""))
    except Exception:
        queue.put(("failed", traceback.format_exc(limit=3).replace("\n", " | ")))


def try_import(path: Path, timeout_seconds: int = 5) -> tuple[str, str]:
    """Best-effort import of a target file using a timed subprocess.

    Spawns a background process to test if the file can be cleanly imported.
    Failure or timeout is reported gracefully instead of halting execution.

    Args:
        path: The Path object pointing to the script to import.
        timeout_seconds: Maximum seconds allowed for the import before termination.

    Returns:
        A tuple of (import_status, import_error_message). Status is 'success' or 'failed'.
    """
    queue: mp.Queue = mp.Queue()
    process = mp.Process(target=_import_worker, args=(str(path), queue))
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        return "failed", f"Import timed out after {timeout_seconds} seconds"
    if not queue.empty():
        return queue.get()
    if process.exitcode == 0:
        return "success", ""
    return "failed", f"Import process exited with code {process.exitcode}"


class ScopeComplexityVisitor(ast.NodeVisitor):
    """Heuristic complexity estimator for one module/function AST scope.

    Traverses the Abstract Syntax Tree (AST) of a code block to track loop depths,
    comprehensions, allocations, and specific mathematical or IO patterns to
    calculate Big-O time and space bounds.
    """

    def __init__(self) -> None:
        """Initializes the complexity visitor trackers and metrics."""
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.has_unbounded_loop = False
        self.loop_count = 0
        self.sort_calls: list[str] = []
        self.comprehensions = 0
        self.recursive_calls = 0
        self.scope_name = ""
        self.collections_allocated = 0
        self.string_accumulation = False
        self.file_or_dataframe_read = False
        self.external_api_or_io = False
        self.dominant: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visits a standard function definition.

        Nested functions are analyzed as part of the parent function because
        their runtime cost is incurred only if the parent creates/calls them.
        """
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visits an asynchronous function definition using standard function rules."""
        self.visit_FunctionDef(node)  # type: ignore[arg-type]

    def visit_For(self, node: ast.For) -> None:
        """Tracks the entry, nesting depth, and exit of a standard for-loop."""
        self.loop_count += 1
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.dominant.append(f"for-loop at line {node.lineno}")
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:
        """Tracks while-loops, flagging explicit infinite loop patterns (while True)."""
        self.loop_count += 1
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            self.has_unbounded_loop = True
            self.dominant.append(f"unbounded while True loop at line {node.lineno}")
        else:
            self.dominant.append(f"while-loop at line {node.lineno}")
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_ListComp(self, node: ast.ListComp) -> None:
        """Notes space allocations and loops triggered by a list comprehension."""
        self.comprehensions += 1
        self.collections_allocated += 1
        self.max_loop_depth = max(self.max_loop_depth, len(node.generators))
        self.dominant.append(f"list comprehension at line {node.lineno}")
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        """Notes space allocations and loops triggered by a set comprehension."""
        self.comprehensions += 1
        self.collections_allocated += 1
        self.max_loop_depth = max(self.max_loop_depth, len(node.generators))
        self.dominant.append(f"set comprehension at line {node.lineno}")
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        """Notes space allocations and loops triggered by a dictionary comprehension."""
        self.comprehensions += 1
        self.collections_allocated += 1
        self.max_loop_depth = max(self.max_loop_depth, len(node.generators))
        self.dominant.append(f"dict comprehension at line {node.lineno}")
        self.generic_visit(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        """Notes implicit loops triggered by a generator expression without direct space cost."""
        self.comprehensions += 1
        self.max_loop_depth = max(self.max_loop_depth, len(node.generators))
        self.dominant.append(f"generator expression at line {node.lineno}")
        self.generic_visit(node)

    def visit_List(self, node: ast.List) -> None:
        """Tracks literal list definitions which allocate space."""
        self.collections_allocated += 1
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        """Tracks literal dictionary definitions which allocate space."""
        self.collections_allocated += 1
        self.generic_visit(node)

    def visit_Set(self, node: ast.Set) -> None:
        """Tracks literal set definitions which allocate space."""
        self.collections_allocated += 1
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """Checks for risky string accumulation (+=) inside of loop structures."""
        if isinstance(node.op, ast.Add) and isinstance(node.target, ast.Name):
            if self.loop_depth > 0:
                self.string_accumulation = True
                self.dominant.append(f"possible accumulation with += at line {node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Intercepts function calls to check for sorting, IO, API usage, or recursion."""
        name = self._call_name(node.func)
        if name in {"sorted", "sort"} or name.endswith(".sort"):
            self.sort_calls.append(name)
            self.dominant.append(f"sort call at line {node.lineno}")
        if name in {"open", "read_csv"} or name.endswith(".read_csv"):
            self.file_or_dataframe_read = True
            self.dominant.append(f"file/dataframe read at line {node.lineno}")
        if any(token in name.lower() for token in ["generate_content", "rawinputstream", "acceptwaveform", "model"]):
            self.external_api_or_io = True
            self.dominant.append(f"external API/audio/model call at line {node.lineno}")
        if self.scope_name and name == self.scope_name:
            self.recursive_calls += 1
            self.dominant.append(f"recursive call at line {node.lineno}")
        self.generic_visit(node)

    @staticmethod
    def _call_name(func: ast.AST) -> str:
        """Extracts a string representation of a callable node identifier.

        Args:
            func: The AST node containing the function call structure.

        Returns:
            The plain text string name of the method/function if resolved, else "".
        """
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            left = ScopeComplexityVisitor._call_name(func.value)
            return f"{left}.{func.attr}" if left else func.attr
        return ""

    def estimate(self) -> tuple[str, str, str, str]:
        """Calculates final complexity heuristic estimates based on collected syntax.

        Returns:
            A tuple containing:
                - time_complexity (e.g., "O(n^2)")
                - space_complexity (e.g., "O(n)")
                - confidence_level ("Low-Medium", "Medium", "Medium-High")
                - compiled_notes_string
        """
        if self.has_unbounded_loop:
            time = "Unbounded / event-driven until user interrupt or quit"
            confidence = "Medium"
        elif self.sort_calls and self.max_loop_depth >= 1:
            time = "O(n log n) or higher, depending on looped sort input"
            confidence = "Low-Medium"
        elif self.max_loop_depth >= 3:
            time = "O(n^3)"
            confidence = "Low-Medium"
        elif self.max_loop_depth == 2:
            time = "O(n^2)"
            confidence = "Medium"
        elif self.max_loop_depth == 1 or self.comprehensions:
            time = "O(n)"
            confidence = "Medium-High"
        else:
            time = "O(1)"
            confidence = "Medium"

        if self.string_accumulation and self.has_unbounded_loop:
            space = "O(n), grows with accumulated transcript/text"
        elif self.collections_allocated or self.file_or_dataframe_read or self.string_accumulation:
            space = "O(n)"
        else:
            space = "O(1)"

        notes: list[str] = []
        if self.has_unbounded_loop:
            notes.append("Contains an explicit while True loop; practical runtime depends on user/session length.")
        if self.external_api_or_io:
            notes.append("Runtime includes external API, audio, model, or device I/O latency that Big-O does not capture.")
        if self.file_or_dataframe_read:
            notes.append("n generally means rows/items read from the CSV or dataframe.")
        if self.max_loop_depth == 2:
            notes.append("Nested loops dominate the estimate.")
        if self.string_accumulation:
            notes.append("Repeated += accumulation may copy growing strings depending on runtime behaviour.")

        return time, space, confidence, " ".join(notes)


def line_end(node: ast.AST) -> int:
    """Safe fallback calculation to find the ending line number of an AST Node.

    Args:
        node: The target AST element.

    Returns:
        The line number integer where the element block closes.
    """
    return int(getattr(node, "end_lineno", getattr(node, "lineno", 1)))


def scope_nodes(tree: ast.Module) -> Iterable[tuple[str, str, ast.AST]]:
    """Yield module-level pseudo-scope and all top-level function/class scopes.

    Groups general script-level operations together under a '<module>' tag, and 
    separates independent structural blocks like functions and methods.

    Args:
        tree: The top-level parsed Abstract Syntax Tree module root.

    Yields:
        A tuple format: (scope_type_string, scope_name_string, scope_ast_node)
    """
    module_body = [node for node in tree.body if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    if module_body:
        pseudo = ast.Module(body=module_body, type_ignores=[])
        setattr(pseudo, "lineno", min(getattr(n, "lineno", 1) for n in module_body))
        setattr(pseudo, "end_lineno", max(line_end(n) for n in module_body))
        yield "module", "<module>", pseudo
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield "function", node.name, node
        elif isinstance(node, ast.ClassDef):
            yield "class", node.name, node
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    yield "method", f"{node.name}.{child.name}", child


def analyze_file(path: Path, import_status: str, import_error: str) -> list[dict[str, str]]:
    """Parses a specific Python file's source code to map out scope complexities.

    Args:
        path: System file path to the source file.
        import_status: Status outcome string from the subprocess loader pipeline.
        import_error: Captured error trace snippet string if imports failed.

    Returns:
        A list of data dictionaries structured to match the target CSV fields.
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    rows: list[dict[str, str]] = []

    for scope_type, scope_name, node in scope_nodes(tree):
        visitor = ScopeComplexityVisitor()
        visitor.scope_name = scope_name.split(".")[-1]
        visitor.visit(node)
        time_complexity, space_complexity, confidence, notes = visitor.estimate()
        rows.append(
            {
                "source_file": path.name,
                "import_status": import_status,
                "import_error": import_error,
                "scope_type": scope_type,
                "scope_name": scope_name,
                "line_start": str(getattr(node, "lineno", 1)),
                "line_end": str(line_end(node)),
                "time_complexity_estimate": time_complexity,
                "space_complexity_estimate": space_complexity,
                "dominant_operations": "; ".join(visitor.dominant[:8]),
                "confidence": confidence,
                "notes": notes,
            }
        )
    return rows


def write_report(path: Path, rows: list[dict[str, str]]) -> Path:
    """Saves structured scope metrics to an isolated CSV report document.

    Args:
        path: Original script file path (used to determine report file name).
        rows: Complete collection of mapped scope rows to dump into the document.

    Returns:
        A Path instance showing where the final CSV document was written.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{path.stem}_complexity.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def main() -> None:
    """Orchestrates loop pipeline execution over all identified source targets.

    Dispatches import processes, fires AST heuristic evaluations, and saves 
    individual validation outputs inside the local file environment.
    """
    print(f"Writing reports to: {OUTPUT_DIR}")
    for filename in TARGET_FILES:
        path = BASE_DIR / filename
        if not path.exists():
            print(f"SKIP missing: {filename}")
            continue
        import_status, import_error = try_import(path)
        rows = analyze_file(path, import_status, import_error)
        output_path = write_report(path, rows)
        print(f"{filename}: {import_status}; wrote {output_path.name}")


if __name__ == "__main__":
    main()