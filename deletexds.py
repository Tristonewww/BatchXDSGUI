import os
import shutil
import sys

def delete_files(directory, target_filename):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower() == target_filename:
                file_path = os.path.join(root, file)
                print(f"Deleting file: {file_path}")
                os.remove(file_path)

def delete_folders(directory, target_foldername):
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir.lower() == target_foldername:
                folder_path = os.path.join(root, dir)
                print(f"Deleting folder: {folder_path}")
                shutil.rmtree(folder_path)


def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]  
        print(f"Deleted XDS files and folders in: {input_path}")
        delete_files(input_path, 'xds.inp')
        delete_folders(input_path, 'xds')
    else:
        print("No input path provided.")

if __name__ == "__main__":
    main()
