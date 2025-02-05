#!/usr/bin/env python3

import argparse
from pathlib import Path
import chardet

def analyze_file(file_path):
    """
    Analyze a file's encoding and provide detailed diagnostics.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        tuple: (is_utf8, diagnostics_dict)
    """
    raw_bytes = Path(file_path).read_bytes()
    
    # Try UTF-8 first
    is_utf8 = True
    error_details = None
    try:
        raw_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        is_utf8 = False
        error_details = str(e)
    
    # Get file details
    file_size = len(raw_bytes)
    
    # If not UTF-8, try to detect the actual encoding
    detected_encoding = chardet.detect(raw_bytes)
    
    # Check for common encoding signatures (BOM)
    bom_info = None
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        bom_info = "UTF-8 BOM detected"
    elif raw_bytes.startswith(b'\xff\xfe'):
        bom_info = "UTF-16 LE BOM detected"
    elif raw_bytes.startswith(b'\xfe\xff'):
        bom_info = "UTF-16 BE BOM detected"
    
    # Sample of problematic bytes if not UTF-8
    problem_sample = None
    if not is_utf8 and error_details:
        # Extract position from error message
        try:
            pos = int(error_details.split('in position')[1].split(':')[0].strip())
            # Get a sample around the problematic byte
            start = max(0, pos - 10)
            end = min(len(raw_bytes), pos + 10)
            problem_bytes = raw_bytes[start:end]
            problem_sample = {
                'position': pos,
                'hex_values': ' '.join(f'{b:02x}' for b in problem_bytes),
                'printable': ''.join(chr(b) if 32 <= b <= 126 else '.' for b in problem_bytes)
            }
        except ValueError:
            pass

    return is_utf8, {
        'file_size': file_size,
        'detected_encoding': detected_encoding,
        'bom_info': bom_info,
        'error_details': error_details,
        'problem_sample': problem_sample
    }

def main():
    parser = argparse.ArgumentParser(description='Check if a file is UTF-8 encoded with detailed diagnostics')
    parser.add_argument('file_path', help='Path to the file to check encoding')
    
    args = parser.parse_args()
    
    try:
        is_utf8, diagnostics = analyze_file(args.file_path)
        
        print(f"\nFile Analysis for: {args.file_path}")
        print("-" * 50)
        
        if is_utf8:
            print("✓ The file is UTF-8 encoded")
        else:
            print("✗ The file is NOT UTF-8 encoded")
        
        print(f"\nFile size: {diagnostics['file_size']} bytes")
        
        if diagnostics['bom_info']:
            print(f"BOM: {diagnostics['bom_info']}")
        
        if not is_utf8:
            print("\nDiagnostics:")
            print(f"Detected encoding: {diagnostics['detected_encoding']['encoding']} "
                  f"(confidence: {diagnostics['detected_encoding']['confidence']:.1%})")
            
            if diagnostics['error_details']:
                print(f"UTF-8 decode error: {diagnostics['error_details']}")
            
            if diagnostics['problem_sample']:
                print("\nProblematic section:")
                print(f"Position: {diagnostics['problem_sample']['position']}")
                print(f"Hex values: {diagnostics['problem_sample']['hex_values']}")
                print(f"Printable: {diagnostics['problem_sample']['printable']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
