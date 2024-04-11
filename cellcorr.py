import os
import sys

def main():
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        print(f"cellcorr has received input path: {folder_path}")

        txt_path = os.path.join(folder_path, "Cell_information.txt")
        print(f"Using txt file: {txt_path}")

        try:
            with open(txt_path, 'r') as file:
                txt_content = file.readlines()
        except FileNotFoundError:
            print(f"Could not find the file: {txt_path}")
            return

        spacegroup_provided_by_user = None
        unitcell_provided_by_user = None

        for line in txt_content:
            if "SPACE_GROUP_NUMBER=" in line:
                spacegroup_provided_by_user = line.strip()
            elif "UNIT_CELL_CONSTANTS=" in line:
                unitcell_provided_by_user = line.strip()

        if not spacegroup_provided_by_user:
            print("There is no crystal information of space group!")
        if not unitcell_provided_by_user:
            print("There is no crystal information of unit cell!")

        # Find and update xds.inp in all folders
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.lower() == "xds.inp":
                    inp_file_path = os.path.join(dirpath, filename)
                    with open(inp_file_path, 'r') as file:
                        inp_content = file.readlines()

                    # Modify the unit cell and space group in xds.inp
                    for i, line in enumerate(inp_content):
                        if "SPACE_GROUP_NUMBER=" in line and spacegroup_provided_by_user:
                            inp_content[i] = spacegroup_provided_by_user + "\n"
                        elif "UNIT_CELL_CONSTANTS=" in line and unitcell_provided_by_user:
                            inp_content[i] = unitcell_provided_by_user + "\n"

                    # Write the changes back to xds.inp
                    with open(inp_file_path, 'w') as file:
                        file.writelines(inp_content)

        print("Finished processing all xds.inp files in the selected folder.")
    else:
        print("No input path provided.")

if __name__ == "__main__":
    main()
