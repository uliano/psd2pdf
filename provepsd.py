#!/usr/bin/env python3

from psd_tools import PSDImage
from PIL import Image, ImageStat
import sys
import os

psd = PSDImage.open('file1.psd')