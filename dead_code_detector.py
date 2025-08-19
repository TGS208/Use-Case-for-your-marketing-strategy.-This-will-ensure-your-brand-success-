#!/usr/bin/env python3
"""
Dead Code Detector

A tool to detect unused files and dead code in a codebase.
Supports multiple programming languages and provides detailed reports.
"""

import os
import ast
import re
import json
import argparse
import fnmatch
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class DeadCodeDetector:
    """Main class for detecting dead code and unused files."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.file_dependencies = defaultdict(set)
        self.defined_symbols = defaultdict(set)
        self.used_symbols = defaultdict(set)
        self.all_files = set()
        
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load configuration from file or use defaults."""
        default_config = {
            "file_extensions": [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".h"],
            "ignore_patterns": ["**/node_modules/**", "**/venv/**", "**/__pycache__/**", "**/build/**", "**/dist/**"],
            "ignore_files": [".gitignore", "README.md", "LICENSE", "requirements.txt", "package.json"],
            "entry_points": ["main.py", "app.py", "index.js", "main.js", "server.js"],
            "exclude_patterns": ["test_*", "*_test.*", "*.test.*", "*.spec.*"]
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
        
        return default_config
    
    def _should_ignore_file(self, file_path: str) -> bool:
        """Check if file should be ignored based on configuration."""
        file_path = os.path.normpath(file_path)
        
        # Check ignore patterns
        for pattern in self.config["ignore_patterns"]:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        
        # Check ignore files
        file_name = os.path.basename(file_path)
        if file_name in self.config["ignore_files"]:
            return True
            
        return False
    
    def _get_file_extension(self, file_path: str) -> str:
        """Get file extension."""
        return Path(file_path).suffix
    
    def _is_supported_file(self, file_path: str) -> bool:
        """Check if file is supported for analysis."""
        extension = self._get_file_extension(file_path)
        return extension in self.config["file_extensions"]
    
    def scan_directory(self, directory: str) -> None:
        """Scan directory for code files."""
        directory = os.path.abspath(directory)
        for root, dirs, files in os.walk(directory):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore_file(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.abspath(os.path.join(root, file))
                if not self._should_ignore_file(file_path) and self._is_supported_file(file_path):
                    self.all_files.add(file_path)
                    self._analyze_file(file_path)
    
    def _analyze_file(self, file_path: str) -> None:
        """Analyze a single file for imports and symbol definitions."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            extension = self._get_file_extension(file_path)
            
            if extension == '.py':
                self._analyze_python_file(file_path, content)
            elif extension in ['.js', '.ts', '.jsx', '.tsx']:
                self._analyze_javascript_file(file_path, content)
            elif extension in ['.java']:
                self._analyze_java_file(file_path, content)
            elif extension in ['.cpp', '.c', '.h']:
                self._analyze_c_cpp_file(file_path, content)
                
        except Exception as e:
            print(f"Warning: Could not analyze file {file_path}: {e}")
    
    def _analyze_python_file(self, file_path: str, content: str) -> None:
        """Analyze Python file for imports and definitions."""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Handle imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_dependency(file_path, alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._add_dependency(file_path, node.module)
                
                # Handle function and class definitions
                elif isinstance(node, ast.FunctionDef):
                    self.defined_symbols[file_path].add(f"function:{node.name}")
                elif isinstance(node, ast.ClassDef):
                    self.defined_symbols[file_path].add(f"class:{node.name}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.defined_symbols[file_path].add(f"variable:{target.id}")
                            
        except SyntaxError:
            # Handle syntax errors gracefully
            pass
    
    def _analyze_javascript_file(self, file_path: str, content: str) -> None:
        """Analyze JavaScript/TypeScript file for imports and definitions."""
        # Simple regex-based analysis for JS/TS
        
        # Find imports
        import_patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            r'import\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                self._add_dependency(file_path, match)
        
        # Find function definitions
        func_patterns = [
            r'function\s+(\w+)\s*\(',
            r'(\w+)\s*:\s*function\s*\(',
            r'const\s+(\w+)\s*=\s*\(',
            r'let\s+(\w+)\s*=\s*\(',
            r'var\s+(\w+)\s*=\s*\('
        ]
        
        for pattern in func_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                self.defined_symbols[file_path].add(f"function:{match}")
        
        # Find class definitions
        class_matches = re.findall(r'class\s+(\w+)', content)
        for match in class_matches:
            self.defined_symbols[file_path].add(f"class:{match}")
    
    def _analyze_java_file(self, file_path: str, content: str) -> None:
        """Analyze Java file for imports and definitions."""
        # Find imports
        import_matches = re.findall(r'import\s+([^;]+);', content)
        for match in import_matches:
            self._add_dependency(file_path, match.strip())
        
        # Find class definitions
        class_matches = re.findall(r'class\s+(\w+)', content)
        for match in class_matches:
            self.defined_symbols[file_path].add(f"class:{match}")
        
        # Find method definitions
        method_matches = re.findall(r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(', content)
        for match in method_matches:
            self.defined_symbols[file_path].add(f"method:{match}")
    
    def _analyze_c_cpp_file(self, file_path: str, content: str) -> None:
        """Analyze C/C++ file for includes and definitions."""
        # Find includes
        include_matches = re.findall(r'#include\s*[<"]([^>"]+)[>"]', content)
        for match in include_matches:
            self._add_dependency(file_path, match)
        
        # Find function definitions
        func_matches = re.findall(r'\w+\s+(\w+)\s*\([^)]*\)\s*{', content)
        for match in func_matches:
            self.defined_symbols[file_path].add(f"function:{match}")
    
    def _add_dependency(self, from_file: str, to_module: str) -> None:
        """Add a dependency between files."""
        # Try to resolve module to actual file
        resolved_file = self._resolve_module_to_file(from_file, to_module)
        if resolved_file:
            self.file_dependencies[from_file].add(resolved_file)
    
    def _resolve_module_to_file(self, from_file: str, module: str) -> Optional[str]:
        """Resolve a module name to an actual file path."""
        # This is a simplified resolution - in practice, this would be more complex
        base_dir = os.path.dirname(from_file)
        
        # Handle relative imports starting with ./ or ../
        if module.startswith('./') or module.startswith('../'):
            module = module[2:] if module.startswith('./') else module
        
        # Try relative imports
        for ext in self.config["file_extensions"]:
            possible_paths = [
                os.path.join(base_dir, f"{module}{ext}"),
                os.path.join(base_dir, module, f"index{ext}"),
                os.path.join(base_dir, module, f"main{ext}")
            ]
            
            for path in possible_paths:
                normalized_path = os.path.normpath(path)
                if os.path.exists(normalized_path) and normalized_path in self.all_files:
                    return normalized_path
        
        return None
    
    def find_unused_files(self) -> Set[str]:
        """Find files that are not imported by any other file."""
        used_files = set()
        entry_points = set()
        
        # Identify entry points
        for file_path in self.all_files:
            file_name = os.path.basename(file_path)
            if any(file_name.startswith(ep.split('.')[0]) for ep in self.config["entry_points"]):
                entry_points.add(file_path)
        
        # If no entry points found, consider all files as potential entry points
        if not entry_points:
            entry_points = self.all_files.copy()
        
        # Build transitive closure of used files
        def mark_used(file_path: str):
            if file_path in used_files:
                return
            used_files.add(file_path)
            for dep in self.file_dependencies.get(file_path, set()):
                mark_used(dep)
        
        for entry_point in entry_points:
            mark_used(entry_point)
        
        # Files that are defined but not used (excluding test files)
        unused_files = set()
        for file_path in self.all_files:
            if file_path not in used_files:
                # Skip test files
                file_name = os.path.basename(file_path)
                is_test = any(fnmatch.fnmatch(file_name, pattern) for pattern in self.config["exclude_patterns"])
                if not is_test:
                    unused_files.add(file_path)
        
        return unused_files
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a detailed report of findings."""
        unused_files = self.find_unused_files()
        
        report = []
        report.append("=" * 60)
        report.append("DEAD CODE DETECTION REPORT")
        report.append("=" * 60)
        report.append(f"Total files analyzed: {len(self.all_files)}")
        report.append(f"Unused files found: {len(unused_files)}")
        report.append("")
        
        if unused_files:
            report.append("UNUSED FILES:")
            report.append("-" * 40)
            for file_path in sorted(unused_files):
                report.append(f"  • {file_path}")
            report.append("")
        
        # Summary by file type
        file_types = defaultdict(int)
        unused_by_type = defaultdict(int)
        
        for file_path in self.all_files:
            ext = self._get_file_extension(file_path)
            file_types[ext] += 1
            if file_path in unused_files:
                unused_by_type[ext] += 1
        
        if file_types:
            report.append("SUMMARY BY FILE TYPE:")
            report.append("-" * 40)
            for ext, total in sorted(file_types.items()):
                unused = unused_by_type[ext]
                percentage = (unused / total * 100) if total > 0 else 0
                report.append(f"  {ext}: {unused}/{total} unused ({percentage:.1f}%)")
            report.append("")
        
        report.append("ANALYSIS COMPLETE")
        report.append("=" * 60)
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"Report saved to: {output_file}")
        
        return report_text


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Detect unused code and dead files in a codebase")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to analyze (default: current directory)")
    parser.add_argument("-c", "--config", help="Configuration file path")
    parser.add_argument("-o", "--output", help="Output file for the report")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist")
        return 1
    
    print(f"Analyzing directory: {args.directory}")
    if args.config:
        print(f"Using config file: {args.config}")
    
    detector = DeadCodeDetector(args.config)
    detector.scan_directory(args.directory)
    
    if args.verbose:
        print(f"Found {len(detector.all_files)} files to analyze")
    
    report = detector.generate_report(args.output)
    
    if not args.output:
        print(report)
    
    return 0


if __name__ == "__main__":
    exit(main())