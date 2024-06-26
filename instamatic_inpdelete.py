import os
import sys
import tkinter as tk
from tkinter import messagebox

def delete_first_7_lines(file_path):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()
            with open(file_path, 'w', encoding=encoding) as file:
                file.writelines(lines[7:])
            break  # Break the loop if the file was successfully read and written
        except UnicodeDecodeError:
            continue  # Try the next encoding if a UnicodeDecodeError occurs

def find_and_modify_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower() == 'xds.inp':
                file_path = os.path.join(root, file)
                print(f"Modifying file: {file_path}")
                delete_first_7_lines(file_path)

def main(): 
    root = tk.Tk()
    root.withdraw()
    
    #Show the messagebox
    user_response = messagebox.askyesno("For instamatic user", 
                                        "Do you really want to modify xds.inp generated by instamatic? This step will delete the first 7 lines in all xds.inp.")
    
    if user_response:
        if len(sys.argv) > 1:
            input_path = sys.argv[1]
            find_and_modify_files(input_path)
            print("All xds.inps have deleted the first 7 lines. Please remember to cite instamatic.")
        else:
            print("No input path provided.")
    else:
        print("Modification cancelled by the user.")

if __name__ == "__main__":
    main()
