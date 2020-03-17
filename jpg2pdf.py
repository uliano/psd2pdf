#!/usr/bin/env python3

from PIL import Image
import sys
import os


def psd2pdf(image_dir: str) -> None:

    files = os.listdir(image_dir)
    files = [file for file in files if file[-5:] in ['.jpeg', '.JPEG'] or file[-4:] in ['.jpg', '.JPG']]
    bases = {''.join(filter(str.isalpha, file.split('.')[0])) for file in files}
    for base in bases:
        out_file = base + '.pdf'
        b_files = [file for file in files if base in file]
        images = [(''.join(filter(str.isdigit, file)), os.path.join(image_dir, file)) for file in b_files]
        images.sort()
        images = [Image.open(image[1]).convert('RGB') for image in images]
        images[0].save(out_file, save_all=True, quality=90, append_images=images[1:])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("I need exactly 1 parameter")
        sys.exit(0)
    the_dir = sys.argv[1]
    if not os.path.isdir(the_dir):
        print(f'{the_dir} not found')
    psd2pdf(the_dir)
