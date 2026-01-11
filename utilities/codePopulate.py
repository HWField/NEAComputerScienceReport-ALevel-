#!/usr/bin/env python3
"""
Code Appendix Generator for LaTeX Report
Generates a beautifully formatted appendix with all code files from a project directory.

LABEL REFERENCE GUIDE:
  Each file in the appendix gets a label you can reference in your document.
  
  Label format: \label{code:path:to:file}
  - Forward slashes (/) in paths are replaced with colons (:)
  - File extensions are included in the label
  
  Examples:
    File: SimulationAPI/Models/Agent.cs
    Label: \label{code:SimulationAPI:Models:Agent.cs}
    
    File: frontend/src/api/simulation.ts  
    Label: \label{code:frontend:src:api:simulation.ts}
  
  How to reference in your document:
    - Use \nameref{code:path:to:file} to show the filename
    - Use Section~\ref{code:path:to:file} to show "Section X.Y.Z"
    - Combine: \nameref{code:path:to:file}, Lines 10--25
"""

import os
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import mimetypes

PROJECT_PATH = Path("/Users/Henry/Desktop/NEAComputerScience/")
OUTPUT_FILE = Path("/Users/Henry/Desktop/CompSciNEA/ComputerScienceNEAReport/Chapters/CodeAppendix.tex")
class CodeAppendixGenerator:
    def __init__(self, project_path: str, output_file: str):
        self.project_path = Path(project_path)
        self.output_file = Path(output_file)
        self.supported_extensions = {
            '.py': 'python',
            '.cs': 'csharp',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.vue': 'vue',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.sql': 'sql',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text',
            '.sh': 'bash',
            '.bat': 'batch'
        }
        self.ignore_dirs = {'.git', '__pycache__', 'node_modules', 'bin', 'obj', '.vs', '.vscode', 'dist', 'build', 'Migrations'}
        self.ignore_files = {'.gitignore', '.DS_Store', 'Thumbs.db'}
        self.ignore_paths = {'frontend/package-lock.json'}  # Specific file paths to exclude
        
    def should_include_file(self, file_path: Path) -> bool:
        """Check if a file should be included in the appendix."""
        if file_path.name in self.ignore_files:
            return False
        
        # Check if the relative path matches any ignored paths
        relative_path = self.get_relative_path(file_path)
        if relative_path in self.ignore_paths:
            return False
        
        # Check if it's a text file and has a supported extension
        if file_path.suffix.lower() in self.supported_extensions:
            return True
            
        # Check if it's a text file without extension (like README, Makefile, etc.)
        if file_path.suffix == '' and file_path.name.upper() in ['README', 'MAKEFILE', 'DOCKERFILE']:
            return True
            
        return False
    
    def get_language_from_extension(self, file_path: Path) -> str:
        """Get the minted language identifier from file extension."""
        ext = file_path.suffix.lower()
        return self.supported_extensions.get(ext, 'text')
    
    def escape_latex_special_chars(self, text: str) -> str:
        """Escape special LaTeX characters in file content."""
        # For minted blocks, we don't need to escape most characters
        # but we should handle some edge cases
        return text
    
    def get_relative_path(self, file_path: Path) -> str:
        """Get relative path from project root."""
        try:
            return str(file_path.relative_to(self.project_path))
        except ValueError:
            return str(file_path)
    
    def organize_files_by_directory(self) -> Dict[str, List[Path]]:
        """Organize files by their directory structure."""
        file_structure = {}
        
        for root, dirs, files in os.walk(self.project_path):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            root_path = Path(root)
            relative_root = self.get_relative_path(root_path)
            
            # Skip if this is an ignored directory
            if any(ignored in root_path.parts for ignored in self.ignore_dirs):
                continue
            
            code_files = []
            for file in files:
                file_path = root_path / file
                if self.should_include_file(file_path):
                    code_files.append(file_path)
            
            if code_files:
                file_structure[relative_root] = sorted(code_files)
        
        return file_structure
    
    def get_section_depth(self, directory: str) -> int:
        """Calculate the depth of a directory for LaTeX sectioning."""
        if directory == '.':
            return 0
        return len(Path(directory).parts)
    
    def get_latex_section_command(self, depth: int) -> str:
        """Get appropriate LaTeX sectioning command based on depth."""
        # depth 0 = section (top-level projects like frontend, SimulationAPI)
        # depth 1 = subsection (e.g., src, Controllers)
        # depth 2 = subsubsection (e.g., api, components)
        # depth 3 = paragraph (e.g., deeper nesting)
        # depth 4+ = subparagraph
        commands = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
        return commands[min(depth, len(commands) - 1)]
    
    def format_directory_name(self, directory: str) -> str:
        """Format directory name for LaTeX display."""
        if directory == '.':
            return "Root Directory"
        return directory.replace('_', r'\_').replace('&', r'\&').replace('%', r'\%')
    
    def format_filename(self, file_path: Path) -> str:
        """Format filename for LaTeX display, without extension."""
        name = file_path.stem  # Removes extension
        return name.replace('_', r'\_').replace('&', r'\&').replace('%', r'\%')
    def read_file_content(self, file_path: Path) -> str:
        """Read file content, handling different encodings."""
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
                return f"% Could not read file: {e}"
        
        return "% Could not decode file with any supported encoding"
    
    def generate_latex_appendix(self) -> str:
        """Generate the complete LaTeX appendix."""
        file_structure = self.organize_files_by_directory()

        latex_content = []
        latex_content.append("\\chapter{Code Listing}")
        latex_content.append("\\label{appendix:code}")
        latex_content.append("")
        latex_content.append("This appendix contains the complete source code for the project, organized by directory structure.")
        latex_content.append("")

        # Get all directories sorted properly
        all_dirs = sorted(file_structure.keys(), key=lambda x: (x.count('/'), x))
        
        # Find top-level directories
        root_key = "." if "." in file_structure else ""
        top_level_dirs = set()
        
        for directory in all_dirs:
            if directory not in (root_key, "", "."):
                top_dir = directory.split('/')[0]
                top_level_dirs.add(top_dir)
        
        # Process each top-level directory as a main section
        for top_dir in sorted(top_level_dirs):
            formatted_top_dir = self.format_directory_name(top_dir)
            latex_content.append(f"\\section{{{formatted_top_dir}}}")
            latex_content.append(f"\\label{{code:{top_dir.replace('/', ':')}}}")
            latex_content.append("")
            
            # Build a tree structure for this top-level directory
            tree = {}
            for directory in all_dirs:
                if directory == top_dir or directory.startswith(top_dir + '/'):
                    tree[directory] = file_structure.get(directory, [])
            
            # Process the tree in proper order
            self._process_directory_tree(tree, top_dir, latex_content, is_root=True)

        return "\n".join(latex_content)
    
    def _process_directory_tree(self, tree: Dict[str, List[Path]], current_dir: str, 
                                 latex_content: List[str], is_root: bool = False):
        """Recursively process directory tree in proper order."""
        if current_dir not in tree:
            return
        
        files = tree[current_dir]
        
        # Get immediate subdirectories (not nested deeper)
        subdirs = []
        for dir_path in tree.keys():
            if dir_path == current_dir:
                continue
            # Check if this is a direct child
            if dir_path.startswith(current_dir + '/'):
                relative = dir_path[len(current_dir) + 1:]
                if '/' not in relative:  # Direct child, not nested deeper
                    subdirs.append(dir_path)
        
        subdirs.sort()
        
        # Add files in current directory first (if not root)
        if files and not is_root:
            for file_path in files:
                self._add_file_to_latex(file_path, latex_content)
        elif files and is_root:
            # For root-level files in top directory, add them as subsections
            for file_path in files:
                filename = self.format_filename(file_path)
                relative_path = self.get_relative_path(file_path)
                language = self.get_language_from_extension(file_path)

                latex_content.append(f"\\subsection{{{filename}}}")
                latex_content.append(f"\\label{{code:{relative_path.replace('/', ':')}}}")
                latex_content.append("")
                latex_content.append(f"\\textbf{{File:}} \\texttt{{{relative_path.replace('_', r'\_')}}}")
                latex_content.append("")

                try:
                    content = self.read_file_content(file_path)
                    if content.strip():
                        latex_content.append(f"\\inputminted[linenos, tabsize=1, breaklines]{{{language}}}{{{file_path}}}")
                    else:
                        latex_content.append("\\begin{center}")
                        latex_content.append("\\textit{(Empty file)}")
                        latex_content.append("\\end{center}")
                except Exception as e:
                    latex_content.append(f"% Error reading file: {e}")
                    latex_content.append("\\begin{center}")
                    latex_content.append(f"\\textit{{(Could not read file: {e})}}")
                    latex_content.append("\\end{center}")

                latex_content.append("")
        
        # Then add subdirectories
        for subdir in subdirs:
            self._add_directory_section(subdir, tree, latex_content)
    
    def _get_dir_depth_from_root(self, directory: str) -> int:
        """Get depth of directory from its top-level parent."""
        parts = directory.split('/')
        return len(parts) - 1  # -1 because first part is the top-level dir
    
    def _add_directory_section(self, directory: str, tree: Dict[str, List[Path]], 
                                latex_content: List[str]):
        """Add a directory section with proper depth."""
        # Get the directory name (last part of path)
        parts = directory.split('/')
        dir_name = parts[-1]
        
        # Calculate depth from top-level
        depth = self._get_dir_depth_from_root(directory)
        
        # Get section command (subsection, subsubsection, paragraph)
        section_cmd = self.get_latex_section_command(depth)
        formatted_dir = self.format_directory_name(dir_name)
        
        latex_content.append(f"\\{section_cmd}{{{formatted_dir}}}")
        latex_content.append(f"\\label{{code:{directory.replace('/', ':')}}}")
        latex_content.append("")
        
        # Add files in this directory
        if directory in tree:
            for file_path in tree[directory]:
                self._add_file_to_latex(file_path, latex_content)
        
        # Get and process subdirectories
        subdirs = []
        for dir_path in tree.keys():
            if dir_path.startswith(directory + '/'):
                relative = dir_path[len(directory) + 1:]
                if '/' not in relative:  # Direct child only
                    subdirs.append(dir_path)
        
        # Process subdirectories recursively
        for subdir in sorted(subdirs):
            self._add_directory_section(subdir, tree, latex_content)
    
    def _add_file_to_latex(self, file_path: Path, latex_content: List[str]):
        """Add a single file to the LaTeX content."""
        filename = self.format_filename(file_path)
        relative_path = self.get_relative_path(file_path)
        language = self.get_language_from_extension(file_path)
        
        # Files use paragraph
        latex_content.append(f"\\paragraph{{{filename}}}")
        latex_content.append(f"\\label{{code:{relative_path.replace('/', ':')}}}")
        latex_content.append("")
        latex_content.append(f"\\textbf{{File:}} \\texttt{{{relative_path.replace('_', r'\_')}}}")
        latex_content.append("")

        try:
            content = self.read_file_content(file_path)
            if content.strip():
                latex_content.append(f"\\inputminted[linenos, tabsize=1, breaklines]{{{language}}}{{{file_path}}}")
            else:
                latex_content.append("\\begin{center}")
                latex_content.append("\\textit{(Empty file)}")
                latex_content.append("\\end{center}")
        except Exception as e:
            latex_content.append(f"% Error reading file: {e}")
            latex_content.append("\\begin{center}")
            latex_content.append(f"\\textit{{(Could not read file: {e})}}")
            latex_content.append("\\end{center}")

        latex_content.append("")
    
    
    def generate_appendix_file(self):
        """Generate the LaTeX appendix file."""
        print(f"Scanning project directory: {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project directory does not exist: {self.project_path}")
        
        latex_content = self.generate_latex_appendix()
        
        # Write to output file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"✅ Appendix generated successfully: {self.output_file}")
        
        # Count files processed
        file_structure = self.organize_files_by_directory()
        total_files = sum(len(files) for files in file_structure.values())
        total_dirs = len(file_structure)
        
        print(f"📁 Processed {total_dirs} directories")
        print(f"📄 Processed {total_files} files")
        print("\nTo include in your main LaTeX document, add:")
        print(f"\\include{{{self.output_file.stem}}}")

def main():
    try:
        print(f"🚀 Starting code appendix generation for project: {PROJECT_PATH}")
        generator = CodeAppendixGenerator(str(PROJECT_PATH), str(OUTPUT_FILE))
        generator.generate_appendix_file()
        print(f"\n✅ Appendix generated successfully at: {OUTPUT_FILE}")
        print(f"To include it in LaTeX, use: \\include{{Chapters/CodeAppendix}}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
