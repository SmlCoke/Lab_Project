# Lab4 Task1 Delay Measurement Automation

This directory contains Python automation scripts for Full Adder delay measurements.

**中文文档**: 请参阅 [快速开始.md](./快速开始.md)

## Files

- `generate_sp.py`: Generate HSPICE testbench files for different input patterns
- `run_sp.py`: Batch run HSPICE simulations
- `parse_delay.py`: Parse simulation results and generate statistics
- `subckt.sp`: Full Adder subcircuit definitions (in Lab4 root directory)

## Workflow

### 1. Generate HSPICE Testbench Files

```bash
# Generate all delay test scripts for both FA16 and FA28
python3 generate_sp.py --fa-type both --output-dir .

# Generate FA16 test scripts only
python3 generate_sp.py --fa-type FA16 --output-dir .

# Generate FA28 test scripts only
python3 generate_sp.py --fa-type FA28 --output-dir .
```

Generated files will be saved in the following directory structure:
```
Task1/
├── FA16/
│   └── delay/
│       ├── FA16_delay_A_to_Sum_B0_Cin0.sp
│       ├── FA16_delay_A_to_Sum_B0_Cin1.sp
│       └── ... (24 test files total)
└── FA28/
    └── delay/
        ├── FA28_delay_A_to_Sum_B0_Cin0.sp
        ├── FA28_delay_A_to_Sum_B0_Cin1.sp
        └── ... (24 test files total)
```

### 2. Run HSPICE Simulations

```bash
# Run all delay tests
python3 run_sp.py --base-dir .

# Run FA16 tests only
python3 run_sp.py --base-dir . --fa-type FA16

# Run FA28 tests only
python3 run_sp.py --base-dir . --fa-type FA28

# Preview files to be processed (dry-run, no actual simulation)
python3 run_sp.py --base-dir . --dry-run
```

Note: Ensure HSPICE is installed and the `hspice` command is available in your PATH.

### 3. Parse Results and Generate Statistics

```bash
# Parse all delay measurement results
python3 parse_delay.py . --output delay_summary

# Specify a different output filename
python3 parse_delay.py . --output my_results
```

This will generate the following files:
- `delay_summary.csv`: Detailed delay measurement data (CSV format)
- `delay_summary.xlsx`: Detailed delay measurement data (Excel format)
- `delay_summary_stats.txt`: Statistical summary (text format)

## Delay Test Patterns

For each input-to-output path of the Full Adder, the scripts test all possible static input combinations:

### Test Paths

1. **A -> Sum**: Measure delay when A input changes and Sum output responds
   - Static input combinations: B=0/1, Cin=0/1 (4 combinations total)

2. **B -> Sum**: Measure delay when B input changes and Sum output responds
   - Static input combinations: A=0/1, Cin=0/1 (4 combinations total)

3. **Cin -> Sum**: Measure delay when Cin input changes and Sum output responds
   - Static input combinations: A=0/1, B=0/1 (4 combinations total)

4. **A -> Cout**: Measure delay when A input changes and Cout output responds
   - Static input combinations: B=0/1, Cin=0/1 (4 combinations total)

5. **B -> Cout**: Measure delay when B input changes and Cout output responds
   - Static input combinations: A=0/1, Cin=0/1 (4 combinations total)

6. **Cin -> Cout**: Measure delay when Cin input changes and Cout output responds
   - Static input combinations: A=0/1, B=0/1 (4 combinations total)

Total: Each Full Adder design (FA16/FA28) has 6 paths × 4 combinations = 24 test cases

### Delay Metrics

Each test case measures three metrics:

- **tpLH**: Low-to-high propagation delay (input rising edge to output rising edge)
- **tpHL**: High-to-low propagation delay (input falling edge to output falling edge)
- **tp**: Average propagation delay = (tpLH + tpHL) / 2

## Results Analysis

After running `parse_delay.py`, you can view results in the following ways:

1. **Detailed Data**: Open `delay_summary.xlsx` to view complete data for each test case
2. **Statistical Summary**: Check `delay_summary_stats.txt` for min, max, and average delays for each path
3. **Custom Analysis**: Use `delay_summary.csv` for further data processing and visualization

## Example Output

Example statistical summary:
```
Delay Measurement Statistics (in picoseconds)
======================================================================

FA16:
  Path                 Min          Max          Avg          Count   
  --------------------------------------------------------------------
  A_to_Cout              25.30        35.40        30.20          4
  A_to_Sum               28.50        42.10        35.80          4
  B_to_Cout              26.10        36.20        31.50          4
  B_to_Sum               29.20        43.50        36.90          4
  Cin_to_Cout            22.40        28.30        25.10          4
  Cin_to_Sum             30.10        38.60        34.20          4

FA28:
  Path                 Min          Max          Avg          Count   
  --------------------------------------------------------------------
  A_to_Cout              27.50        38.20        32.60          4
  A_to_Sum               32.40        46.80        39.50          4
  ...
```

## References

These scripts were designed with reference to the following Lab3 scripts:
- `DIC/Lab3/parser_mt.py`: .mt file parsing methods
- `DIC/Lab3/Task2/generate_sp.py`: .sp script generation template
- `DIC/Lab3/Task2/run_sp.py`: Batch HSPICE execution methods

## Notes

1. Ensure HSPICE is properly installed and configured before running simulations
2. Simulation time depends on the number of test cases and system performance; please be patient
3. If some simulations fail, check the corresponding .lis files for error messages
4. Generated intermediate files (.tr0, .ic0, .st0, etc.) can be deleted to save space if needed
