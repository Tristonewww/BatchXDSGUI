#Please ignore. Path delivery test
import sys
def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]  
        print(f"xdsrunner has received input path: {input_path}")
    else:
        print("No input path provided.")

if __name__ == "__main__":
    main()



###mrc2img
import os
import sys
from pathlib import Path
import numpy as np
import fabio
import mrcfile

def conversion(directory):
    converted_frames = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mrc'):
                mrc_path = os.path.join(root, file)
                img_path = os.path.splitext(mrc_path)[0] + '.img'

                with mrcfile.open(mrc_path) as mrc:
                    img_data = mrc.data

                pedestal = img_data + 500
                pedestal[pedestal > 65000] = 65000
                pedestal[pedestal < 0] = 0

                img = fabio.adscimage.AdscImage(data=pedestal.astype(np.uint16))
                img.header['SIZE1'] = 2048
                img.header['SIZE2'] = 2048
                img.header['PIXEL_SIZE'] = 0.028
                img.write(img_path)

                print(f"Converted {mrc_path} to {img_path}")
                converted_frames += 1

    return converted_frames

def main(directory):
    if not directory:
        print("No directory selected. Exiting.")
        sys.exit(1)

    converted_frames = conversion(directory)
    print(f"Frames converted: {converted_frames}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        main(directory)
    else:
        print("No directory provided. Please provide a directory as an argument.")
