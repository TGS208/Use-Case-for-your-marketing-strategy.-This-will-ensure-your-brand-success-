# Dead Code Detector

A powerful tool to detect unused code and dead files in your codebase. This tool helps maintain clean, efficient codebases by identifying files, functions, classes, and variables that are defined but never used.

## Features

- **Multi-language support**: Python, JavaScript, TypeScript, Java, C/C++, and more
- **Unused file detection**: Identifies files that are not imported or referenced by other files
- **Dead code analysis**: Finds unused functions, classes, and variables within files
- **Configurable**: Customizable file patterns, ignore rules, and entry points
- **Detailed reporting**: Comprehensive reports with statistics and breakdown by file type
- **Entry point detection**: Automatically identifies application entry points

## Installation

No installation required! This is a standalone Python script that works with Python 3.6+.

## Quick Start

1. **Basic usage** - Analyze current directory:
   ```bash
   python3 dead_code_detector.py
   ```

2. **Analyze specific directory**:
   ```bash
   python3 dead_code_detector.py /path/to/your/project
   ```

3. **Use custom configuration**:
   ```bash
   python3 dead_code_detector.py -c dead_code_config.json
   ```

4. **Save report to file**:
   ```bash
   python3 dead_code_detector.py -o report.txt
   ```

## Configuration

Create a `dead_code_config.json` file to customize the analysis:

```json
{
    "file_extensions": [".py", ".js", ".ts", ".java"],
    "ignore_patterns": ["**/node_modules/**", "**/venv/**"],
    "ignore_files": ["README.md", "LICENSE"],
    "entry_points": ["main.py", "app.py", "index.js"],
    "exclude_patterns": ["*test*", "*.test.*"]
}
```

### Configuration Options

- **file_extensions**: File types to analyze
- **ignore_patterns**: Directory patterns to ignore (supports wildcards)
- **ignore_files**: Specific files to ignore
- **entry_points**: Files that serve as application entry points
- **exclude_patterns**: Patterns for test files and other files to exclude from unused file detection

## Examples

The `examples/` directory contains sample code in different languages to demonstrate the tool:

- `examples/python/` - Python examples with unused functions and orphaned files
- `examples/javascript/` - JavaScript examples with dead code patterns

### Running Examples

```bash
# Analyze Python examples
python3 dead_code_detector.py examples/python

# Analyze JavaScript examples  
python3 dead_code_detector.py examples/javascript

# Analyze all examples
python3 dead_code_detector.py examples
```

## Supported Languages

| Language   | File Extensions | Features Supported |
|------------|----------------|-------------------|
| Python     | .py            | ✅ Imports, functions, classes, variables |
| JavaScript | .js, .jsx      | ✅ Imports/requires, functions, classes |
| TypeScript | .ts, .tsx      | ✅ Imports, functions, classes |
| Java       | .java          | ✅ Imports, classes, methods |
| C/C++      | .c, .cpp, .h   | ✅ Includes, functions |

## How It Works

1. **File Discovery**: Scans directories for supported file types
2. **Dependency Analysis**: Parses imports, requires, and includes to build dependency graph
3. **Symbol Detection**: Identifies function, class, and variable definitions
4. **Usage Analysis**: Determines which files are referenced and which symbols are used
5. **Dead Code Identification**: Finds files and symbols that are defined but never used
6. **Report Generation**: Creates detailed reports with findings and statistics

## Command Line Options

```
python3 dead_code_detector.py [options] [directory]

Positional arguments:
  directory             Directory to analyze (default: current directory)

Optional arguments:
  -h, --help           Show help message
  -c, --config CONFIG  Configuration file path
  -o, --output OUTPUT  Output file for the report
  -v, --verbose        Verbose output
```

## Understanding the Report

The tool generates reports with the following sections:

1. **Summary**: Total files analyzed and unused files found
2. **Unused Files**: List of files that are not imported by other files
3. **File Type Breakdown**: Statistics by file extension showing unused percentages

Example report:
```
============================================================
DEAD CODE DETECTION REPORT
============================================================
Total files analyzed: 8
Unused files found: 2

UNUSED FILES:
----------------------------------------
  • examples/javascript/orphaned-module.js
  • examples/python/orphaned_module.py

SUMMARY BY FILE TYPE:
----------------------------------------
  .js: 1/4 unused (25.0%)
  .py: 1/4 unused (25.0%)

ANALYSIS COMPLETE
============================================================
```

## Best Practices

1. **Regular Analysis**: Run the tool regularly as part of your CI/CD pipeline
2. **Review Before Deletion**: Always review flagged files before deleting them
3. **Custom Configuration**: Tailor the configuration to your project structure
4. **Entry Points**: Ensure all application entry points are properly configured
5. **Test Files**: Use exclude patterns to avoid flagging legitimate test files

## Limitations

- **Dynamic Imports**: May not detect dynamically loaded modules
- **Reflection**: Cannot analyze reflection-based usage patterns
- **External Dependencies**: Only analyzes local project files
- **Language Variants**: Some language-specific features may not be fully supported

## Contributing

This tool can be extended to support additional languages and analysis patterns. Key areas for improvement:

- Enhanced module resolution logic
- Support for more programming languages
- Better handling of dynamic code patterns
- Integration with build systems and IDEs

## License

This tool is provided as-is for educational and development purposes.