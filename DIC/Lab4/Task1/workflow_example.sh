#!/bin/bash
# Complete workflow example for Lab4 Task1 delay measurement automation
# This script demonstrates the full automation pipeline

echo "======================================================================"
echo "Lab4 Task1 Delay Measurement Automation Workflow"
echo "======================================================================"
echo ""

# Step 1: Generate HSPICE test files
echo "Step 1: Generating HSPICE test files..."
echo "----------------------------------------------------------------------"
python3 generate_sp.py --fa-type both --output-dir .
echo ""
echo "✓ Generated 48 test files (24 for FA16, 24 for FA28)"
echo ""

# Step 2: Run HSPICE simulations (dry-run first to verify)
echo "Step 2: Verifying files to be simulated (dry-run)..."
echo "----------------------------------------------------------------------"
python3 run_sp.py --base-dir . --dry-run
echo ""

# Uncomment the following line to actually run HSPICE simulations
# Note: This requires HSPICE to be installed and available in PATH
echo "To run actual HSPICE simulations, execute:"
echo "  python3 run_sp.py --base-dir ."
echo ""
echo "Or run simulations for a specific FA type:"
echo "  python3 run_sp.py --base-dir . --fa-type FA16"
echo "  python3 run_sp.py --base-dir . --fa-type FA28"
echo ""

# Step 3: Parse results (requires simulation to be completed)
echo "Step 3: After HSPICE simulations complete, parse results with:"
echo "----------------------------------------------------------------------"
echo "  python3 parse_delay.py . --output delay_summary"
echo ""
echo "This will generate:"
echo "  - delay_summary.csv: Detailed delay measurements"
echo "  - delay_summary.xlsx: Excel format of detailed data"
echo "  - delay_summary_stats.txt: Statistical summary"
echo ""

echo "======================================================================"
echo "Workflow Complete!"
echo "======================================================================"
echo ""
echo "Quick Reference:"
echo "  1. Generate .sp files:  python3 generate_sp.py --fa-type both"
echo "  2. Run simulations:     python3 run_sp.py --base-dir ."
echo "  3. Parse results:       python3 parse_delay.py ."
echo ""
echo "For more details, see README.md"
echo ""
