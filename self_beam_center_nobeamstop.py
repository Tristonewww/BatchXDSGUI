import os
import sys
import numpy as np
import fabio
from scipy import ndimage

def find_img_files(folder_path):
    """Search for .img files within a specified folder path."""
    print(f"Searching for .img files in {folder_path}")
    img_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.img'):
                img_files.append(os.path.join(root, file))
    print(f"Found {len(img_files)} .img files.")
    return img_files

def find_direct_beam_center(img_path):
    """Find the approximate center of the direct beam in an .img file."""
    img = fabio.open(img_path)
    img_array = img.data
    max_intensity = np.max(img_array)
    max_position = np.unravel_index(np.argmax(img_array), img_array.shape)
    threshold = max_intensity * 0.2
    bright_mask = img_array > threshold
    if np.any(bright_mask):
        center_y, center_x = ndimage.center_of_mass(bright_mask)
    else:
        center_y, center_x = max_position
    print(f"Center of direct beam located at ({center_x}, {center_y})")
    return center_y, center_x

def process_folder(folder_path):
    img_files = find_img_files(folder_path)
    if not img_files:
        print("No .img files found in this folder.")
        return None

    total_x, total_y, valid_imgs = 0, 0, 0
    for img_file in img_files:
        y, x = find_direct_beam_center(img_file)
        if x > 0 and y > 0:
            total_x += x
            total_y += y
            valid_imgs += 1

    if valid_imgs > 0:
        avg_x = total_x / valid_imgs
        avg_y = total_y / valid_imgs
        print(f"Average beam center position: ({avg_x}, {avg_y})")
        # Determine the path for the beam centers file based on the first .img file
        img_directory = os.path.dirname(img_files[0])
        update_beam_centers_file(img_directory, avg_x, avg_y)
        update_xds_inp(img_directory, avg_x, avg_y)
    else:
        print("Unable to calculate average beam center.")

def update_beam_centers_file(img_directory, avr_x, avr_y):
    """Write the average beam center to a text file in the image directory."""
    centers_file_path = os.path.join(img_directory, 'direct_beam_centers.txt')
    with open(centers_file_path, 'w') as file:
        file.write(f"Average beam center: ({avr_x}, {avr_y})\n")

def update_xds_inp(img_directory, avr_x, avr_y):
    """Update the ORGX and ORGY values in the xds.inp file located in the 'xds' subfolder."""
    xds_inp_path = os.path.join(img_directory, 'xds', 'xds.inp')
    if os.path.exists(xds_inp_path):
        with open(xds_inp_path, 'r') as file:
            lines = file.readlines()
        lines = [line for line in lines if not line.startswith('ORGX=') and not line.startswith('ORGY=')]
        with open(xds_inp_path, 'w') as file:
            file.writelines(lines)
            file.write(f'ORGX={avr_x} ORGY={avr_y}\n')
        print(f"xds.inp successfully updated with ORGX={avr_x}, ORGY={avr_y}.")
    else:
        print(f"xds.inp not found at the expected path: {xds_inp_path}")

def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        print(f"Self beam center finding has received input path: {input_path}")
        for folder_name in sorted(os.listdir(input_path)):
            folder_path = os.path.join(input_path, folder_name)
            if os.path.isdir(folder_path):
                print(f"Entering folder: {folder_path}")
                process_folder(folder_path)
            else:
                print(f"{folder_path} is not a directory.")
    else:
        print("No input path provided.")

if __name__ == "__main__":
    main()