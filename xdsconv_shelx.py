import os
import subprocess
import sys

def main(input_path):
    # Ensure input path is provided
    if not input_path:
        print("No input path provided.")
        return

    # Define the xprep directory path inside the input path
    xprep_dir = os.path.join(input_path, "merge")

    # Ensure xprep directory exists
    if not os.path.exists(xprep_dir):
        print(f"xprep directory does not exist at {xprep_dir}")
        return

    # Search for the all.hkl file in the xprep directory, ignoring case sensitivity
    for file in os.listdir(xprep_dir):
        if file.lower() == "all.hkl":
            all_hkl_path = os.path.join(xprep_dir, file)
            break
    else:
        print("all.hkl file not found in the xprep directory.")
        return

    # Read the all.hkl file and search for the unit cell constants
    with open(all_hkl_path, 'r') as hkl_file:
        for line in hkl_file:
            if line.startswith("!UNIT_CELL_CONSTANTS="):
                # Extract unit cell constants after the "=" sign
                xprep_unitcell = line.split('=')[1].strip()
                break
        else:
            print("!UNIT_CELL_CONSTANTS= not found in the all.hkl file.")
            return

    # Create 1.P4P file with the unit cell constants
    with open(os.path.join(xprep_dir, "1.P4P"), 'w') as p4p_file:
        p4p_file.write(f"CELL {xprep_unitcell}")

    # Create XDSCONV.INP file with specified content
    xdscov_inp_content = """OUTPUT_FILE= 1.HKL SHELX
INPUT_FILE= all.HKL     !format is XDS_ASCII by default
FRIEDEL'S_LAW=TRUE
!MERGE=FALSE
"""
    with open(os.path.join(xprep_dir, "XDSCONV.INP"), 'w') as inp_file:
        inp_file.write(xdscov_inp_content)

    # Run XSCALE in the merge directory
    subprocess.run(["xdsconv"], cwd=xprep_dir)

    # Print completion message
    print("XDS.HKL has been converted into 1.hkl with 1.p4p. Run xprep 1 to check data in shelx.")

if __name__ == "__main__":
    # Obtain the input path from the command line argument
    input_path = sys.argv[1] if len(sys.argv) > 1 else ""
    main(input_path)
