# Code Appendix Generator - Usage Guide

TO RUN
cd /Users/Henry/Desktop/CompSciNEA/ComputerScienceNEAReport/utilities && python3 codePopulate.py /Users/Henry/Desktop/NEAComputerScience/ -o ../Chapters/CodeAppendix.tex

## Overview

This Python script automatically generates a beautifully formatted LaTeX appendix containing all your project's source code, organized by folder structure.

## Features

- ✅ Recursive directory scanning
- ✅ Automatic language detection based on file extensions
- ✅ Beautiful LaTeX formatting with syntax highlighting
- ✅ Proper sectioning based on folder depth
- ✅ Ignores common build/cache directories
- ✅ Handles multiple text encodings
- ✅ Cross-references and labels for easy navigation

## Supported Languages

- Python (.py)
- C# (.cs)
- TypeScript (.ts)
- JavaScript (.js)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- HTML (.html)
- CSS (.css)
- SQL (.sql)
- JSON (.json)
- XML (.xml)
- YAML (.yaml, .yml)
- Markdown (.md)
- Shell scripts (.sh)
- Batch files (.bat)

## Usage

### Method 1: Command Line

```bash
cd utilities
python3 codePopulate.py /path/to/your/project -o ../Chapters/CodeAppendix.tex
```

### Method 2: Using the Shell Script

1. Edit `generate_appendix.sh` and update the `PROJECT_PATH` variable
2. Run the script:

```bash
cd utilities
./generate_appendix.sh
```

### Method 3: Interactive

```bash
cd utilities
python3 codePopulate.py
# Follow the prompts
```

## Command Line Arguments

- `project_path`: Path to your project directory (required)
- `-o, --output`: Output LaTeX file name (default: CodeAppendix.tex)

## Example Commands

### For a local project:

```bash
python3 codePopulate.py ~/Documents/MyProject -o ../Chapters/CodeAppendix.tex
```

### For a web project:

```bash
python3 codePopulate.py ~/WebDev/MyWebsite -o ../Chapters/WebCodeAppendix.tex
```

## Output Structure

The generated LaTeX file will have this structure:

```
Chapter: Code Listing
├── Section: Root Directory
│   ├── Subsection: file1.py
│   └── Subsection: file2.js
├── Section: src
│   ├── Subsection: main.py
│   └── Subsection: utils.py
├── Section: src/components
│   ├── Subsection: Button.tsx
│   └── Subsection: Modal.tsx
└── Section: tests
    └── Subsection: test_main.py
```

## Features in Detail

### Intelligent File Filtering

- Automatically ignores build directories (bin/, obj/, node_modules/, etc.)
- Skips system files (.DS_Store, Thumbs.db, etc.)
- Only includes text-based source code files

### Beautiful Formatting

- Each file gets its own subsection with clear labeling
- Syntax highlighting using LaTeX `minted` package
- File paths shown as typewriter text
- Proper cross-referencing for navigation

### Error Handling

- Gracefully handles unreadable files
- Multiple encoding support (UTF-8, Latin-1, etc.)
- Clear error messages for debugging

## Integration with Your Report

The script automatically updates your `Main.tex` to include:

```latex
\appendix
\include{Chapters/CodeAppendix}
```

## Tips for Best Results

1. **Clean your project first**: Remove unnecessary build files and temporary directories
2. **Use meaningful folder names**: They become section headings in your appendix
3. **Add comments to your code**: They'll appear in the LaTeX output
4. **Test compilation**: Make sure your LaTeX setup supports the `minted` package

## Troubleshooting

### LaTeX compilation errors:

- Ensure you have the `minted` package installed
- Compile with `pdflatex -shell-escape` to enable minted
- Check that Python's `pygments` is installed for syntax highlighting

### Python errors:

- Make sure you're using Python 3.6+
- Check that the project path exists and is accessible
- Verify file permissions for the output directory

### Large projects:

- The script automatically adds page breaks between files
- Consider excluding very large files manually if needed
- LaTeX may take longer to compile with many code files

## Customization

You can modify the script to:

- Add support for new file extensions
- Change the LaTeX formatting
- Modify which directories/files to ignore
- Adjust the sectioning depth

Look for these variables in the code:

- `supported_extensions`: Add new language mappings
- `ignore_dirs`: Add directories to skip
- `ignore_files`: Add specific files to skip
