#!/usr/bin/env python3
"""
Parse HSPICE .mt0 files and extract delay measurements.

This script extends the parser_mt.py functionality from Lab3 to specifically
handle delay measurement results and generate summary statistics.
"""

import pandas as pd
import argparse
import re
import os
from pathlib import Path

# Constants
SECONDS_TO_PICOSECONDS = 1e12  # Conversion factor from seconds to picoseconds


def parse_mt(filepath):
    """
    Parse HSPICE .mt0 file and extract measurement data.
    
    This is adapted from DIC/Lab3/parser_mt.py
    
    Args:
        filepath: Path to the .mt0 file
    
    Returns:
        pandas DataFrame with measurement results
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.rstrip() for line in f if line.strip()]

    # Find .TITLE line
    title_idx = None
    for i, line in enumerate(lines):
        if line.startswith('.TITLE'):
            title_idx = i
            break
    
    if title_idx is None:
        raise ValueError(f"Could not find .TITLE line: {filepath}")

    # Extract data section
    data_start = title_idx + 1
    data_lines = []
    for line in lines[data_start:]:
        if line.startswith('$') or line.startswith('.END'):
            break
        data_lines.append(line)

    # Identify multi-line headers
    header_lines = []
    data_start_idx = 0
    for i, line in enumerate(data_lines):
        # Check if this line starts with numbers (data begins)
        if re.match(r'^\s*[-\d]', line):
            data_start_idx = i
            break
        header_lines.append(line)

    # Merge multi-line headers
    header_text = ' '.join(header_lines)
    headers = re.findall(r'[A-Za-z0-9_\#\+\-\(\)\/]+', header_text)
    
    # Extract data rows
    data_part = data_lines[data_start_idx:]
    rows = []
    current_row = []
    for line in data_part:
        # Match floating point or integer numbers (including scientific notation)
        tokens = re.findall(r'[-+]?\d*\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+(?:[eE][-+]?\d+)?', line)
        if not tokens:
            continue
        current_row.extend(tokens)
        # Check if row is complete
        if len(current_row) >= len(headers):
            rows.append(current_row[:len(headers)])
            current_row = current_row[len(headers):]

    df = pd.DataFrame(rows, columns=headers)

    # Convert to numeric types
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except Exception:
            pass

    return df


def parse_delay_file(sp_file):
    """
    Parse a delay measurement file and extract key information.
    
    Args:
        sp_file: Path to the .sp file (will look for corresponding .mt0)
    
    Returns:
        Dictionary with parsed information, or None if parsing failed
    """
    sp_path = Path(sp_file)
    
    # Construct .mt0 filename
    mt0_file = sp_path.with_suffix('.mt0')
    
    if not mt0_file.exists():
        return None
    
    # Parse the .mt0 file
    try:
        df = parse_mt(mt0_file)
    except Exception as e:
        print(f"Error parsing {mt0_file}: {e}")
        return None
    
    # Extract information from folder name
    # Format: InputSignal_InitialState_FinalState_OutputSignal
    # Example: CI_100_101_CO or A_000_100_S
    folder_name = sp_path.parent.name
    parts = folder_name.split('_')
    
    if len(parts) != 4:
        print(f"Warning: Unexpected folder name format: {folder_name}")
        return None
    
    # Parse folder name components
    input_map = {'A': 'A', 'B': 'B', 'CI': 'Cin'}
    output_map = {'S': 'Sum', 'CO': 'Cout'}
    
    input_signal = input_map.get(parts[0], parts[0])
    initial_state = parts[1]  # e.g., "100"
    final_state = parts[2]     # e.g., "101"
    output_signal = output_map.get(parts[3], parts[3])
    
    # Parse initial and final states (format: ABC where A, B, C are binary digits)
    def parse_state(state_str):
        return {
            'A': int(state_str[0]),
            'B': int(state_str[1]),
            'Cin': int(state_str[2])
        }
    
    initial = parse_state(initial_state)
    final = parse_state(final_state)
    
    # Get FA type from the filename
    fa_type = sp_path.stem  # FA16 or FA28
    
    # Extract delay measurements from dataframe
    result = {
        'fa_type': fa_type,
        'input': input_signal,
        'output': output_signal,
        'initial_state': initial,
        'final_state': final,
        'folder_name': folder_name,
    }
    
    # Extract tpLH, tpHL, and tp values if they exist
    if 'tpLH' in df.columns and len(df) > 0:
        result['tpLH'] = df['tpLH'].iloc[0]
    
    if 'tpHL' in df.columns and len(df) > 0:
        result['tpHL'] = df['tpHL'].iloc[0]
    
    if 'tp' in df.columns and len(df) > 0:
        result['tp'] = df['tp'].iloc[0]
    
    return result


def parse_all_delay_files(base_dir, pattern='delay'):
    """
    Parse all delay measurement files in the specified directory.
    
    Args:
        base_dir: Base directory to search
        pattern: Subdirectory pattern to match (default: 'delay')
    
    Returns:
        List of dictionaries with parsed results
    """
    results = []
    base_path = Path(base_dir)
    
    # Find all 'delay' subdirectories and recursively search for .sp files
    for delay_dir in base_path.rglob(pattern):
        if delay_dir.is_dir():
            # Recursively find all .sp files under this directory
            for sp_file in sorted(delay_dir.rglob('*.sp')):
                result = parse_delay_file(sp_file)
                if result and 'tp' in result:  # Only include if we have delay data
                    results.append(result)
    
    return results


def create_summary_dataframe(results):
    """
    Create a summary DataFrame from parsed results.
    
    Args:
        results: List of dictionaries from parse_all_delay_files
    
    Returns:
        pandas DataFrame with organized results
    """
    rows = []
    
    for r in results:
        # Create a row with all relevant information
        row = {
            'FA_Type': r['fa_type'],
            'Input': r['input'],
            'Output': r['output'],
            'Initial_State': f"{r['initial_state']['A']}{r['initial_state']['B']}{r['initial_state']['Cin']}",
            'Final_State': f"{r['final_state']['A']}{r['final_state']['B']}{r['final_state']['Cin']}",
        }
        
        # Add initial state values individually
        row['Init_A'] = r['initial_state']['A']
        row['Init_B'] = r['initial_state']['B']
        row['Init_Cin'] = r['initial_state']['Cin']
        
        # Add final state values individually
        row['Final_A'] = r['final_state']['A']
        row['Final_B'] = r['final_state']['B']
        row['Final_Cin'] = r['final_state']['Cin']
        
        # Add delay measurements
        if 'tpLH' in r:
            row['tpLH_ps'] = r['tpLH'] * SECONDS_TO_PICOSECONDS
        if 'tpHL' in r:
            row['tpHL_ps'] = r['tpHL'] * SECONDS_TO_PICOSECONDS
        if 'tp' in r:
            row['tp_ps'] = r['tp'] * SECONDS_TO_PICOSECONDS
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df


def generate_statistics(df):
    """
    Generate statistics for each input->output path.
    
    Args:
        df: DataFrame from create_summary_dataframe
    
    Returns:
        Dictionary with statistics
    """
    stats = {}
    
    for fa_type in df['FA_Type'].unique():
        stats[fa_type] = {}
        fa_df = df[df['FA_Type'] == fa_type]
        
        for input_sig in df['Input'].unique():
            for output_sig in df['Output'].unique():
                key = f"{input_sig}_to_{output_sig}"
                path_df = fa_df[(fa_df['Input'] == input_sig) & (fa_df['Output'] == output_sig)]
                
                if len(path_df) > 0 and 'tp_ps' in path_df.columns:
                    stats[fa_type][key] = {
                        'min_tp': path_df['tp_ps'].min(),
                        'max_tp': path_df['tp_ps'].max(),
                        'avg_tp': path_df['tp_ps'].mean(),
                        'count': len(path_df)
                    }
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Parse HSPICE delay measurement results and generate statistics.'
    )
    parser.add_argument(
        'base_dir',
        type=str,
        help='Base directory containing delay measurement results'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='delay_summary',
        help='Output filename prefix (without extension, default: delay_summary)'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default='delay',
        help='Subdirectory pattern to match (default: "delay")'
    )
    
    args = parser.parse_args()
    
    print(f"Parsing delay measurement files in {args.base_dir}...")
    
    # Parse all delay files
    results = parse_all_delay_files(args.base_dir, args.pattern)
    
    if not results:
        print("No delay measurement results found!")
        return
    
    print(f"Found {len(results)} delay measurement results")
    
    # Create summary DataFrame
    df = create_summary_dataframe(results)
    
    # Save detailed results
    csv_path = Path(args.base_dir) / f"{args.output}.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nDetailed results saved to: {csv_path}")
    
    excel_path = Path(args.base_dir) / f"{args.output}.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Detailed results saved to: {excel_path}")
    
    # Generate and save statistics
    stats = generate_statistics(df)
    
    print(f"\n{'='*70}")
    print("Delay Measurement Statistics (in picoseconds)")
    print(f"{'='*70}")
    
    for fa_type, paths in stats.items():
        print(f"\n{fa_type}:")
        print(f"  {'Path':<20} {'Min':<12} {'Max':<12} {'Avg':<12} {'Count':<8}")
        print(f"  {'-'*68}")
        for path, values in sorted(paths.items()):
            print(f"  {path:<20} {values['min_tp']:>10.2f}  {values['max_tp']:>10.2f}  "
                  f"{values['avg_tp']:>10.2f}  {values['count']:>6}")
    
    # Save statistics to text file
    stats_path = Path(args.base_dir) / f"{args.output}_stats.txt"
    with open(stats_path, 'w') as f:
        f.write("Delay Measurement Statistics (in picoseconds)\n")
        f.write("="*70 + "\n\n")
        for fa_type, paths in stats.items():
            f.write(f"{fa_type}:\n")
            f.write(f"  {'Path':<20} {'Min':<12} {'Max':<12} {'Avg':<12} {'Count':<8}\n")
            f.write(f"  {'-'*68}\n")
            for path, values in sorted(paths.items()):
                f.write(f"  {path:<20} {values['min_tp']:>10.2f}  {values['max_tp']:>10.2f}  "
                       f"{values['avg_tp']:>10.2f}  {values['count']:>6}\n")
            f.write("\n")
    
    print(f"\nStatistics saved to: {stats_path}")
    print(f"\n{'='*70}")


if __name__ == '__main__':
    main()
