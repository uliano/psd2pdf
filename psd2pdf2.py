#!/usr/bin/env python3

from psd_tools import PSDImage
from PIL import Image, ImageStat
import sys
import os


def get_masks(an_image: Image) -> PSDImage:
    alpha = an_image.split()[-1]
    bg = Image.new('RGBA', an_image.size, (0, 0, 0, 255))
    bg.paste(alpha, mask=alpha)
    return bg.convert('L')


def psd2pdf(psd_file: str) -> None:
    pdf_file = psd_file[:-4] + '.pdf'
    psd = PSDImage.open(psd_file)
    size = psd.width, psd.height
    layers = {}
    pages = []
    for layer in psd:
        number = ''.join(filter(str.isdigit, layer.name))
        img = layer.topil()
        if img:
            var = sum(ImageStat.Stat(img).var)
            if var:
                layers[number] = img
    layer_numbers = list(layers.keys())
    layer_numbers.sort(key=lambda x: int(x))
    for page_num in layer_numbers:
        image = Image.new('RGBA', size, color='white')
        base_layer = layers[page_num]
        base_image = Image.composite(base_layer, image, get_masks(base_layer))
        pages.append(base_image.convert('RGB'))
    pages[0].save(pdf_file, save_all=True, quality=90, append_images=pages[1:])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("I need exactly 1 parameter")
        sys.exit(0)
    the_file = sys.argv[1]
    if the_file[-4:] != '.psd':
        print(f"{the_file} is not a psd file")
        sys.exit(0)
    if not os.path.isfile(the_file):
        print(f'{the_file} not found')
    psd2pdf(the_file)
