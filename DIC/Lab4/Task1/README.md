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
├── FA16/delay/
│   ├── A_000_100_S/FA16.sp    (A: 000→100, output: Sum)
│   ├── A_001_101_CO/FA16.sp   (A: 001→101, output: Cout)
│   ├── CI_100_101_CO/FA16.sp  (Cin: 100→101, output: Cout)
│   └── ... (18 test folders total)
└── FA28/delay/
    ├── A_000_100_S/FA28.sp
    ├── A_001_101_CO/FA28.sp
    └── ... (18 test folders total)
```

Each test case is in its own folder named: `InputSignal_InitialState_FinalState_OutputSignal`
- Input signals: `A`, `B`, `CI` (for Cin)
- State format: ABC (3 binary digits representing A, B, Cin values)
- Output signals: `S` (Sum), `CO` (Cout)

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

For each input-to-output path of the Full Adder, the scripts test specific transition patterns:

### Test Paths

**For Sum output (12 patterns per FA type):**

1. **A → Sum**: 4 transition patterns
   - A transitions from 0→1 with all combinations of B and Cin static values
   - Examples: `000→100`, `001→101`, `010→110`, `011→111`

2. **B → Sum**: 4 transition patterns  
   - B transitions from 0→1 with all combinations of A and Cin static values
   - Examples: `000→010`, `001→011`, `100→110`, `101→111`

3. **Cin → Sum**: 4 transition patterns
   - Cin transitions from 0→1 with all combinations of A and B static values
   - Examples: `000→001`, `010→011`, `100→101`, `110→111`

**For Cout output (6 patterns per FA type - specific transitions only):**

4. **A → Cout**: 2 specific transition patterns
   - `001→101` (when B=0, Cin=1)
   - `010→110` (when B=1, Cin=0)

5. **B → Cout**: 2 specific transition patterns
   - `100→110` (when A=1, Cin=0)
   - `001→011` (when A=0, Cin=1)

6. **Cin → Cout**: 2 specific transition patterns
   - `100→101` (when A=1, B=0)
   - `010→011` (when A=0, B=1)

**Total**: Each Full Adder design has 12 + 6 = **18 test cases**

Note: For Sum output, all input combinations affect the output, so all 4 transitions are tested per input signal. For Cout output, only specific input combinations cause transitions, so only 2 critical patterns per input signal are tested.

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
