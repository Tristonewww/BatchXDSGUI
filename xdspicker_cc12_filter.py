import sys
import pandas as pd

def main():
    if len(sys.argv) < 3:
        print("Usage: python xdspicker_cc12_filter.py <input_path> <cc12_value>")
        sys.exit(1)

    directory_path = sys.argv[1]  # Directory path received from GUI    
    
    # Attempt to parse the cc12 value as a float
    try:
        xdspicker_cc12_value = float(sys.argv[2])  # cc12 value received from GUI
    except ValueError:
        print("Please enter a correct value!")
        sys.exit(1)

    # Construct the full path to the Excel file
    excel_file_path = directory_path.rstrip('/') + '/xdsrunner2.xlsx'

    try:
        # Load the Excel file from the constructed path
        df = pd.read_excel(excel_file_path, engine='openpyxl')

        # cc12 values are in the 6th column (index 5)
        cc12_column_index = 6

        # Filter rows where the 6th column (cc12) is a number and greater than xdspicker_cc12_value
        df_filtered = df[pd.to_numeric(df.iloc[:, cc12_column_index], errors='coerce').gt(xdspicker_cc12_value)]

        # Save the filtered DataFrame to a new Excel file in the same directory
        output_path = directory_path.rstrip('/') + '/xdspicker.xlsx'
        df_filtered.to_excel(output_path, index=False)

        print(f"cc1/2 filtering completed and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()