import sys
import os
import shutil
import openpyxl  
import pandas as pd
import subprocess
import numpy as np
from types import SimpleNamespace
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("Usage: python exclude_data_clusters.py <input_path> <exclude_data>")
        return

    input_path = sys.argv[1]
    exclude_data = sys.argv[2].split()  # Split the exclude data by spaces
    # Directly convert each input value to an integer and adjust for 1-based indexing
    rows_to_exclude = [int(x) + 1 for x in exclude_data]
    print(f"Received input path: {input_path}")
    print(f"Rows to exclude: {rows_to_exclude}")

    selected_data_dir = os.path.join(input_path, "merge", "selected_data")
    os.makedirs(selected_data_dir, exist_ok=True)

    xdspicker_file = None
    for file in os.listdir(os.path.join(input_path)):
        if file.lower() == "xdspicker.xlsx":
            xdspicker_file = file
            shutil.copy(os.path.join(input_path, file), selected_data_dir)
            print("xdspicker.xlsx has been found and copied.")
            break

    if not xdspicker_file:
        print("xdspicker.xlsx file not found.")
        return

    # Modify xdspicker.xlsx based on exclude data
    xlsx_path = os.path.join(selected_data_dir, "xdspicker.xlsx")
    workbook = openpyxl.load_workbook(xlsx_path)
    sheet = workbook.active
    
    # Since rows are deleted, the indexing will change. Start deleting from the last row.
    for row in sorted(rows_to_exclude, reverse=True):
        sheet.delete_rows(row)

    workbook.save(xlsx_path)
    print("Specified rows have been deleted from xdspicker.xlsx.")

if __name__ == "__main__":
    main()

#xdscale
def main(input_path):
    # Ensure input path is provided
    if not input_path:
        print("No input path provided.")
        return

    # Create the merge directory inside the input path
    merge_dir = os.path.join(input_path, "merge","selected_data")
    os.makedirs(merge_dir, exist_ok=True)

    # Path to the xdspicker.xlsx file
    xlsx_file_path = os.path.join(input_path,"merge","selected_data", "xdspicker.xlsx")
    
    # Read the contents of the xlsx file
    df = pd.read_excel(xlsx_file_path, engine="openpyxl")

    # Check if the DataFrame is empty or does not have enough rows
    if df.empty or len(df) < 2:
        print("The xdspicker is empty or does not have enough datasets. Please check your xdspicker.xlsx")
        return

    # Calculate the average unit cell constants
    unit_cell_data = []
    for index, row in df.iterrows():
        cell_value = row[4]  # Assuming unit cell data is in the 5th column (index 4)
        if isinstance(cell_value, str):
            values = [float(x) for x in cell_value.split()]
        else:
            values = [float(cell_value)]

        # Ensure that each row contributes exactly 6 values
        if len(values) == 6:
            unit_cell_data.extend(values)
        else:
            print(f"Row {index} does not have exactly 6 unit cell values. Skipping this row.")

    if not unit_cell_data or len(unit_cell_data) % 6 != 0:
        print("Unit cell data is not in the correct format or incomplete.")
        return

    # Reshape the unit cell data and compute the average
    unit_cell_df = pd.DataFrame(np.array(unit_cell_data).reshape(-1, 6))
    ave_unitcell_from_all = unit_cell_df.mean(axis=0)
    ave_unitcell_str = " ".join(["{:.2f}".format(x) for x in ave_unitcell_from_all])

    # Create an XSCALE.inp file in the merge directory
    inp_file_path = os.path.join(merge_dir, "XSCALE.inp")
    with open(inp_file_path, "w") as inp_file:
        space_group_number = df.iloc[1, 3]  # Read the value of cell C2
        i_crystals_name = 1
        inp_file.write(f"SPACE_GROUP_NUMBER= {space_group_number}\n")
        inp_file.write(f"UNIT_CELL_CONSTANTS= {ave_unitcell_str}\n\n")
        inp_file.write("OUTPUT_FILE=all.HKL\n")
        inp_file.write("FRIEDEL'S_LAW=TRUE MERGE=FALSE\n")
        inp_file.write("STRICT_ABSORPTION_CORRECTION=FALSE\n")


        for index, row in df.iterrows():
            try:
                resolution = float(row.iloc[8])  # Transfer to float
            except ValueError:
                continue  # If not, skip

            # Continues writing
            inp_file.write("\n")
            inp_file.write(f"!{row.iloc[0]}\n")
            inp_file.write(f"INPUT_FILE={row.iloc[1]}/XDS_ASCII.HKL\n")
            inp_file.write(f"INCLUDE_RESOLUTION_RANGE=200 {resolution}\n")
            inp_file.write("CORRECTIONS= DECAY MODULATION ABSORPTION\n")
            inp_file.write(f"CRYSTAL_NAME=a{index + 1}\n")


    print("XSCALE.inp created successfully!")

    # Run XSCALE in the merge directory
    subprocess.run(["xscale"], cwd=merge_dir)
    print("All data from xdspicker has been merged.")

if __name__ == "__main__":
    # Obtain the input path from the command line argument
    input_path = sys.argv[1] if len(sys.argv) > 1 else ""
    main(input_path)


#bus to shelx
def main(input_path):
    # Ensure input path is provided
    if not input_path:
        print("No input path provided.")
        return

    # Define the xprep directory path inside the input path
    xprep_dir = os.path.join(input_path, "merge","selected_data")

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

#clustering
def find_xscale_lp_file(input_path):
    merge_dir = Path(input_path) / "merge" / "selected_data"
    for file in merge_dir.iterdir():
        if file.name.lower() == "xscale.lp":
            return file
    return None

def parse_xscale_lp_initial(fn="XSCALE.LP"):
    with open(fn, "r") as f:
        spgr, cell, fns, ccs = None, None, {}, []
        reading_filenames, reading_correlations = False, False
        
        for line in f:
            # Parse space group and unit cell constants
            if line.startswith(" SPACE_GROUP_NUMBER="):
                spgr = line.strip()
            elif line.startswith(" UNIT_CELL_CONSTANTS="):
                cell = line.strip()

            # Detect and parse filenames
            elif "READING INPUT REFLECTION DATA FILES" in line:
                reading_filenames = True
                # Skip header lines
                for _ in range(4): next(f)
            elif reading_filenames:
                if "******************************************************************************" in line:
                    reading_filenames = False
                    continue  # Exit filenames reading mode
                line = line.strip()
                inp = line.split()
                if len(inp) == 5:
                    idx = int(inp[0]) - 1  # Adjust for 1-indexing in XSCALE
                    fns[idx] = inp[4]
            
            # Detect and parse correlation coefficients
            elif "CORRELATIONS BETWEEN INPUT DATA SETS AFTER CORRECTIONS" in line:
                reading_correlations = True
                # Skip header lines
                for _ in range(4): next(f)
            elif reading_correlations:
                if not line.strip():  # End of correlation data
                    reading_correlations = False
                    break
                ccs.append(line.strip())

    # Process correlation coefficients
    ccs_data = np.array([line.split() for line in ccs], dtype=float)
    i, j = ccs_data[:, 0].astype(int) - 1, ccs_data[:, 1].astype(int) - 1  # Adjust indices for 0-based indexing
    cc_values = ccs_data[:, 3]  # Assuming the fourth column contains correlation values

    n = max(max(i), max(j)) + 1
    corrmat = np.zeros((n, n))
    for index, value in zip(zip(i, j), cc_values):
        corrmat[index] = value
    corrmat += corrmat.T  # Mirror the values to make the matrix symmetric
    np.fill_diagonal(corrmat, 1.0)  # Fill the diagonal with 1s

    # Return a structured object containing parsed data
    obj = SimpleNamespace(filenames=fns, correlation_matrix=corrmat, unit_cell=cell, space_group=spgr)
    return obj


def calculate_dendrogram(parsed_data):
    # Check if the correlation matrix is not empty and contains data
    if parsed_data.correlation_matrix.size == 0:
        raise ValueError("Correlation matrix is empty.")
    
    corrmat = parsed_data.correlation_matrix
    # Convert correlation matrix to distance matrix for dendrogram calculation
    dmat = np.sqrt(1 - corrmat**2)
    # Condense the distance matrix since linkage function expects condensed form
    tri_upper = np.triu_indices_from(dmat, k=1)
    condensed_dmat = dmat[tri_upper]

    return condensed_dmat


def plot_dendrogram(distance_matrix):
    # Calculate the linkage matrix
    z = linkage(distance_matrix, method="average")
    
    # Determine the number of points based on the linkage matrix
    n = len(z) + 1
    
    # Generate labels starting from 1 to n
    labels = [str(i) for i in range(1, n + 1)]
    
    # Plot the dendrogram with custom labels
    plt.figure(figsize=(10, 7))  # Optional: Adjust the figure size
    dendrogram(z, labels=labels)
    plt.title("Dendrogram")
    plt.xlabel("Dataset index")
    plt.ylabel("Distance")
    
    # Save the plot to a file
    plt.savefig("dendrogram.png")
    
    plt.show()

def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        print(f"xdswriter has received input path: {input_path}")

        xscale_lp_path = find_xscale_lp_file(input_path)
        if xscale_lp_path:
            print(f"Found xscale.lp at: {xscale_lp_path}")
            ccs = parse_xscale_lp_initial(xscale_lp_path)
            # Check if correlation coefficients were found
            if not ccs:  # This checks if the list is empty
                print("No correlation coefficients found in xscale.lp.")
                return  # Exit the function early since there's no data to process
                
            distance_matrix = calculate_dendrogram(ccs)
            plot_dendrogram(distance_matrix)
        else:
            print("xscale.lp not found in the merge directory.")
    else:
        print("No input path provided.")

if __name__ == "__main__":
    main()
