# File Encoding Checker

A Python script to check and diagnose character encoding issues in files, with a focus on UTF-8 validation.

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <repo-directory>
```

2. Install the required dependencies:

```bash
pip install requirements.txt
```

## Usage

Run the script by providing the path to your file:

```bash
python main.py path/to/your/file.csv
```

## Understanding the Output

The script provides detailed information about your file's encoding:

### For UTF-8 Files

If your file is properly UTF-8 encoded, you'll see:

```
File Analysis for: path/to/your/file.csv
--------------------------------------------------
✓ The file is UTF-8 encoded
File size: 1234 bytes
```

### For Non-UTF-8 Files

If your file is not UTF-8 encoded, you'll see detailed diagnostics:

```
File Analysis for: path/to/your/file.csv
--------------------------------------------------
✗ The file is NOT UTF-8 encoded
File size: 1234 bytes

Diagnostics:
Detected encoding: iso-8859-1 (confidence: 92.3%)
UTF-8 decode error: 'utf-8' codec can't decode byte 0xe9 in position 145...

Problematic section:
Position: 145
Hex values: 61 62 63 e9 64 65 66 67 68 69
Printable: abc.defghi
```

The output includes:

- File size in bytes
- Detected encoding and confidence level
- Location and details of the first UTF-8 validation error
- A sample of the problematic section showing:
  - Position: Where the error occurred in the file
  - Hex values: The raw byte values around the error
  - Printable: Human-readable version of the bytes

If you're not sure what to do with this, try sharing the output with ChatGPT along with the file, and asking it to help you fix the file.

## Acting on the Results

If your file is not UTF-8 encoded, here are the steps to fix it:

### Using Python

```python
# Read with the detected encoding (e.g., 'latin1', 'iso-8859-1', etc.)
with open('your_file.csv', 'r', encoding='detected_encoding') as f:
    content = f.read()

# Save as UTF-8
with open('your_file_utf8.csv', 'w', encoding='utf-8') as f:
    f.write(content)
```

### Using Command Line (Unix/Mac)

```bash
# Replace 'ISO-8859-1' with the detected encoding
iconv -f ISO-8859-1 -t UTF-8 input.csv > output_utf8.csv
```

### Common Encoding Issues

1. **Latin-1/ISO-8859-1 Characters**: If you see bytes like `e9` representing characters like 'é', your file is likely in Latin-1 encoding.
2. **Windows-1252**: Similar to Latin-1 but with additional characters in the 128-159 range.

3. **UTF-8 with BOM**: If the script detects a BOM (Byte Order Mark), it will be shown in the output. This is generally fine but some systems might need the BOM removed.

## Best Practices

1. Always make a backup of your files before converting encodings.
2. Verify the converted file works correctly in your application.
3. When creating new files, explicitly specify UTF-8 encoding to prevent issues.

## Troubleshooting

If you're getting unexpected results:

1. Check if your file has a BOM (Byte Order Mark)
2. Verify the detected encoding confidence level
3. Try opening the file in a text editor that shows encoding (like Notepad++ or VS Code)
4. For very large files, check if the encoding is consistent throughout the file
