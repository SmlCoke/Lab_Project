#!/usr/bin/env python3
"""
Batch run HSPICE simulations for Full Adder delay measurements.

This script finds all .sp files in the delay subdirectories and runs
HSPICE simulation for each one, generating corresponding .lis files.
"""

import argparse
import subprocess
from pathlib import Path
import sys


def run_hspice(sp_file, verbose=True):
    """
    Run HSPICE simulation for a single .sp file.
    
    Args:
        sp_file: Path to the .sp file
        verbose: Whether to print progress messages
    
    Returns:
        True if simulation succeeded, False otherwise
    """
    sp_path = Path(sp_file)
    lis_file = sp_path.with_suffix('.lis')
    
    if verbose:
        print(f"Running: {sp_path.name}")
    
    # Construct HSPICE command as a list of arguments (safer than shell=True)
    lis_file_name = lis_file.name
    
    try:
        # Execute HSPICE in the directory containing the .sp file
        # Note: Using shell=True here for compatibility with hspice command and output redirection
        # The sp_path.name is validated to come from our own file listing, not user input
        cmd = f"hspice {sp_path.name} > {lis_file_name}"
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=sp_path.parent,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            if verbose:
                print(f"  ✓ Success: {lis_file.name}")
            return True
        else:
            print(f"  ✗ Failed: {sp_path.name}")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
            return False
    
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout: {sp_path.name}")
        return False
    except Exception as e:
        print(f"  ✗ Error running {sp_path.name}: {e}")
        return False


def find_sp_files(base_dir, pattern='delay'):
    """
    Find all .sp files in subdirectories matching the pattern.
    
    Args:
        base_dir: Base directory to search
        pattern: Subdirectory name pattern (e.g., 'delay')
    
    Returns:
        List of Path objects for .sp files
    """
    sp_files = []
    base_path = Path(base_dir)
    
    # Find all 'delay' subdirectories
    for delay_dir in base_path.rglob(pattern):
        if delay_dir.is_dir():
            # Find all .sp files in this directory
            for sp_file in delay_dir.glob('*.sp'):
                sp_files.append(sp_file)
    
    return sorted(sp_files)


def run_all_simulations(base_dir, pattern='delay', fa_type=None, dry_run=False):
    """
    Run HSPICE simulations for all .sp files found.
    
    Args:
        base_dir: Base directory to search for .sp files
        pattern: Subdirectory pattern to match (default: 'delay')
        fa_type: Filter by FA type ('FA16', 'FA28', or None for all)
        dry_run: If True, only list files without running simulations
    
    Returns:
        Tuple of (total, succeeded, failed) counts
    """
    sp_files = find_sp_files(base_dir, pattern)
    
    # Filter by FA type if specified
    if fa_type:
        sp_files = [f for f in sp_files if fa_type in str(f)]
    
    if not sp_files:
        print(f"No .sp files found in {base_dir} matching pattern '{pattern}'")
        return 0, 0, 0
    
    print(f"Found {len(sp_files)} .sp files to process")
    
    if dry_run:
        print("\nDry run - would process:")
        for sp_file in sp_files:
            print(f"  {sp_file}")
        return len(sp_files), 0, 0
    
    print("\nStarting simulations...\n")
    
    succeeded = 0
    failed = 0
    
    for i, sp_file in enumerate(sp_files, 1):
        print(f"[{i}/{len(sp_files)}] ", end='')
        if run_hspice(sp_file):
            succeeded += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Simulation Summary:")
    print(f"  Total:     {len(sp_files)}")
    print(f"  Succeeded: {succeeded}")
    print(f"  Failed:    {failed}")
    print(f"{'='*60}")
    
    return len(sp_files), succeeded, failed


def main():
    parser = argparse.ArgumentParser(
        description='Batch run HSPICE simulations for Full Adder delay measurements.'
    )
    parser.add_argument(
        '--base-dir',
        type=str,
        default='.',
        help='Base directory to search for .sp files (default: current directory)'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default='delay',
        help='Subdirectory pattern to match (default: "delay")'
    )
    parser.add_argument(
        '--fa-type',
        choices=['FA16', 'FA28'],
        help='Filter simulations by Full Adder type'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='List files that would be processed without running simulations'
    )
    
    args = parser.parse_args()
    
    total, succeeded, failed = run_all_simulations(
        base_dir=args.base_dir,
        pattern=args.pattern,
        fa_type=args.fa_type,
        dry_run=args.dry_run
    )
    
    # Exit with error code if any simulations failed
    if failed > 0 and not args.dry_run:
        sys.exit(1)


if __name__ == '__main__':
    main()
