import os
import pandas as pd
import subprocess
import sys
import numpy as np

def main(input_path):
    # Ensure input path is provided
    if not input_path:
        print("No input path provided.")
        return

    # Create the merge directory inside the input path
    merge_dir = os.path.join(input_path, "merge")
    os.makedirs(merge_dir, exist_ok=True)

    # Path to the xdspicker.xlsx file
    xlsx_file_path = os.path.join(input_path, "xdspicker.xlsx")
    
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
