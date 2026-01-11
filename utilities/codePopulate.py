#!/usr/bin/env python3
"""
LaTeX Code Appendix Generator (Indexed + Folder Counts)

Features:
- One appendix chapter
- Clickable nested index
- Frontend / Backend master trees
- Unlimited folder depth
- Folder file counts (recursive)
- Flat, clean code listings with labels + minted
"""

from pathlib import Path
import os

# =======================
# CONFIGURATION
# =======================

PROJECT_ROOT = Path("/Users/Henry/Desktop/NEAComputerScience/")
OUTPUT_FILE = Path(
    "/Users/Henry/Desktop/CompSciNEA/ComputerScienceNEAReport/Chapters/CodeAppendix.tex"
)

SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".cs": "csharp",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".sql": "sql",
    ".html": "html",
    ".css": "css",
    ".vue": "vue",
    ".md": "markdown",
}
#     ".json": "json", removed to avoid large lock files

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "bin",
    "obj",
    "dist",
    "build",
    ".vs",
    ".vscode",
    "Migrations",
    ".VSCodeCounter",
}

IGNORE_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "package-lock.json",
    "auto-imports.d.ts",
    "components.d.ts",
}

FRONTEND_PREFIX = "frontend/"

# =======================
# HELPERS
# =======================

def latex_escape(text: str) -> str:
    return (
        text.replace("_", r"\_")
            .replace("&", r"\&")
            .replace("%", r"\%")
    )

def label_for_path(rel_path: str) -> str:
    return "code:" + rel_path.replace("/", ":")

def is_code_file(path: Path) -> bool:
    if path.name in IGNORE_FILES:
        return False
    return path.suffix.lower() in SUPPORTED_EXTENSIONS

def language_for(path: Path) -> str:
    return SUPPORTED_EXTENSIONS.get(path.suffix.lower(), "text")

# =======================
# TREE BUILDING
# =======================

def insert_into_tree(tree: dict, parts: list, rel_path: str):
    if not parts:
        return
    head = parts[0]
    if len(parts) == 1:
        tree.setdefault("_files", []).append(rel_path)
    else:
        subtree = tree.setdefault(head, {})
        insert_into_tree(subtree, parts[1:], rel_path)

def build_tree(paths):
    tree = {}
    for rel_path in paths:
        parts = rel_path.split("/")
        insert_into_tree(tree, parts, rel_path)
    return tree

def count_files(tree: dict) -> int:
    """Recursively count all files in this subtree."""
    total = len(tree.get("_files", []))
    for key, subtree in tree.items():
        if key != "_files":
            total += count_files(subtree)
    return total

# =======================
# LATEX EMISSION
# =======================

def emit_tree(tree: dict, indent: int = 0) -> list[str]:
    lines = []
    pad = "  " * indent
    lines.append(f"{pad}\\begin{{itemize}}")

    # folders
    for key in sorted(k for k in tree.keys() if k != "_files"):
        subtree = tree[key]
        file_count = count_files(subtree)
        display = f"{latex_escape(key)} ({file_count} file{'s' if file_count != 1 else ''})"

        lines.append(f"{pad}  \\item \\texttt{{{display}}}")
        lines.extend(emit_tree(subtree, indent + 2))

    # files
    for file in sorted(tree.get("_files", [])):
        label = label_for_path(file)
        name = latex_escape(file.split("/")[-1])
        lines.append(
            f"{pad}  \\item \\nameref{{" + label + "}"
        )

    lines.append(f"{pad}\\end{{itemize}}")
    return lines

def emit_code_listing(rel_path: str) -> list[str]:
    abs_path = PROJECT_ROOT / rel_path
    label = label_for_path(rel_path)
    language = language_for(abs_path)
    name = latex_escape(rel_path.split("/")[-1])
    lines = []
    lines.append(r"\makeatletter")
    lines.append(r"\subsection*{" + name + "}")
    lines.append(latex_escape(rel_path))
    lines.append(r"\phantomsection")
    lines.append(r"\def\@currentlabelname{" + name + "}")
    lines.append(r"\label{" + label + "}")
    lines.append(r"\makeatother")
    lines.append("")
    lines.append(
        r"\inputminted[linenos,breaklines,tabsize=2]{"
        + language + "}{" + str(abs_path) + "}"
    )
    lines.append("")
    return lines

# =======================
# MAIN GENERATION
# =======================

def collect_files():
    frontend = []
    backend = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            path = Path(root) / f
            if not is_code_file(path):
                continue
            rel = path.relative_to(PROJECT_ROOT).as_posix()
            if rel.startswith(FRONTEND_PREFIX):
                frontend.append(rel)
            else:
                backend.append(rel)

    return frontend, backend

def generate():
    frontend, backend = collect_files()

    frontend_tree = build_tree(frontend)
    backend_tree = build_tree(backend)

    out = []

    # ===== Chapter =====
    out.append(r"\chapter{Code Listings}")
    out.append(r"\label{appendix:code}")
    out.append("")
    out.append("This appendix contains the complete source code for the project.")
    out.append("")

    # ===== Index =====
    out.append(r"\section{Index}")
    out.append(r"\textbf{Frontend}")
    out.extend(emit_tree(frontend_tree))
    out.append("")
    out.append(r"\textbf{Backend}")
    out.extend(emit_tree(backend_tree))
    out.append(r"\newpage")

    # ===== Listings =====
    out.append(r"\section{Frontend}")
    for f in sorted(frontend):
        out.extend(emit_code_listing(f))

    out.append(r"\section{Backend}")
    for f in sorted(backend):
        out.extend(emit_code_listing(f))

    OUTPUT_FILE.write_text("\n".join(out), encoding="utf-8")
    print(f"✅ Appendix written to {OUTPUT_FILE}")

# =======================
# ENTRY POINT
# =======================

if __name__ == "__main__":
    generate()