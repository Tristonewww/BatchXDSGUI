import sys
import os
from types import SimpleNamespace
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from pathlib import Path

def find_xscale_lp_file(input_path):
    merge_dir = Path(input_path) / "merge"
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
