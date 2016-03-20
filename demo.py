# coding = utf-8
from __future__ import print_function, division
import os
import math
from PIL import Image

path = '/Volumes/cherrotdisk/Image/2015/04.26_Hope u never grow old/darktable/'
base_name = '04.26_LUO2341.jpg'
file_list = [
    item for item in os.listdir(path)
    if item.endswith(('.jpg', '.png', '.bmp', '.jpeg')) and item != base_name
]

div = int(math.floor(math.sqrt(len(file_list))))
base = Image.open(path + base_name)
# base = base.resize(scale_size, Image.ANTIALIAS)
old_w, old_h = base.size
# whole width and height
w, h = old_w - old_w % div, old_h - old_h % div
# grid width and height
width, height = w // div, h // div

x, y = int((old_w - w) / 2), int((old_h - h) / 2),
base = base.crop((x, y, x + w, y + h))


for i in range(div):
    for j in range(div):
        chunk = Image.open(path + file_list[i * div + j])
        old_chunk_w, old_chunk_h = chunk.size
        if old_chunk_w / old_chunk_h > w / h:
            chunk_h = min(old_chunk_h, h)
            chunk_w = int(round(w / h * chunk_h))
        else:
            chunk_w = min(old_chunk_w, w)
            chunk_h = int(round(h / w * chunk_w))
        x, y = int((old_chunk_w - chunk_w) / 2), int((old_chunk_h - chunk_h) / 2)
        chunk = chunk.crop((x, y, old_chunk_w - x, old_chunk_h - y))

        chunk = chunk.resize((width, height), Image.ANTIALIAS)

        box = (i * width, j * height, i * width + width, j * height + height)
        src_chunk = base.crop(box)
        blend = Image.blend(src_chunk, chunk, 0.3)
        base.paste(blend, box)

base.show()
