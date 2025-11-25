#!/bin/bash
# Example usage script for codePopulate.py

# Change to the directory containing this script
cd "$(dirname "$0")"

# Generate appendix for SimulationAPI project
PROJECT_PATH="/Users/Henry/Desktop/NEAComputerScience/"
OUTPUT_FILE="../Chapters/CodeAppendix.tex"

echo "🚀 Generating code appendix..."
echo "Project path: $PROJECT_PATH"
echo "Output file: $OUTPUT_FILE"

python3 codePopulate.py "$PROJECT_PATH" -o "$OUTPUT_FILE"

echo "✅ Done! Don't forget to include the appendix in your main LaTeX file:"
echo "Add this line before \\end{document}:"
echo "\\include{Chapters/CodeAppendix}"