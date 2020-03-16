#!/usr/bin/env python3

from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer
from PIL import Image, ImageStat
import sys
import os


def get_masks(an_image: Image) -> PSDImage:
    alpha = an_image.split()[-1]
    bg = Image.new('RGBA', an_image.size, (0, 0, 0, 255))
    bg.paste(alpha, mask=alpha)
    return bg.convert('L')


psd_file = sys.argv[1]

if len(sys.argv) != 2:
    print("I need exactly 1 parameter")
    sys.exit(0)

if psd_file[-4:] != '.psd':
    print(f"{psd_file} is not a psd file")
    sys.exit(0)

if not os.path.isfile(psd_file):
    print(f'{psd_file} not found')

pdf_file = psd_file[:-4]+'.pdf'

psd = PSDImage.open(psd_file)
size = psd.width, psd.height
mask = Image.new("L", size, 0)

layers = {}

pages = []

for layer in psd:
    number = ''.join(filter(str.isdigit, layer.name))
    img = layer.topil()
    if img:
        var = sum(ImageStat.Stat(img).var)
        if var:
            layers[number] = img
            print(number)

layer_numbers = list(layers.keys())

base_layers = [layer for layer in layer_numbers if len(layer) == 1]

for page_num in base_layers:
    image = Image.new('RGBA', size, color='white')
    base_layer = layers[page_num]

    pages_num = [(p, layers[p]) for p in layers if len(p) == 2 and p[0] == page_num]
    pages_num.sort()
    to_compose = []
    for p in pages_num:
        to_compose.append(p)

    base_image = Image.composite(base_layer, image, get_masks(base_layer))
    mask = get_masks(base_layer)
    if not to_compose:
        pages.append(base_image.convert('RGB'))
        # base_image.save(page_num + '.png')
    for layer_num, layer in to_compose:
        the_image = Image.composite(layer, base_image, get_masks(layer))
        # the_image.save(layer_num+'.png')
        pages.append(the_image.convert('RGB'))

pages[0].save(pdf_file, save_all=True, quality=90, append_images=pages[1:])
