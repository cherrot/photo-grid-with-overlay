# coding = utf-8
from __future__ import print_function, division
import os
import math
from PIL import Image

path = '/Volumes/cherrotdisk/Image/2015/04.26_Hope u never grow old/darktable/'
base_name = '04.26_LUO2341.jpg'
file_list = [item for item in os.listdir(path) if item.endswith(('.jpg', '.png', '.bmp', '.jpeg')) and item != base_name]

div = int(math.floor(math.sqrt(len(file_list))))
base = Image.open(path + base_name)
old_w, old_h = base.size
w, h = old_w - old_w % div, old_h - old_h % div
cropped = base.crop((
    int((old_w - w) / 2),
    int((old_h - h) / 2),
    int(old_w - (old_w - w) / 2),
    int(old_h - (old_h - h) / 2)
))

chunk_w, chunk_h = w // div, h // div

for i in range(div):
    for j in range(div):
        chunk = Image.open(path + file_list[i * div + j])
        old_chunk_w, old_chunk_h = chunk.size
        if old_chunk_w / old_chunk_h > w / h:
            chunk = chunk.crop((
                int((old_chunk_w - w) / 2),
                0,
                int(old_chunk_w - (old_chunk_w - w) / 2),
                h
            ))
        else:
            chunk = chunk.crop((
                0,
                int((old_chunk_h - h) / 2),
                w,
                int(old_chunk_h - (old_chunk_h - h) / 2)
            ))

        chunk.thumbnail((chunk_w, chunk_h))

        box = (i * chunk_w, j * chunk_h, i * chunk_w + chunk_w, j * chunk_h + chunk_h)
        src_chunk = base.crop(box)
        blend = Image.blend(src_chunk, chunk, 0.4)
        base.paste(blend, box)

base.show()
