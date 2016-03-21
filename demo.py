# coding = utf-8
from __future__ import print_function, division
import os
import math
from PIL import Image
from multiprocessing import Pool, cpu_count

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


def proc_blender(image_path, i, j):
    chunk = Image.open(image_path)
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

    box = (i * width, j * height, (i + 1) * width, (j + 1) * height)
    src_chunk = base.crop(box)
    blend = Image.blend(src_chunk, chunk, 0.3)
    return blend, box

pool = Pool(cpu_count())

procs = [
    [pool.apply_async(proc_blender, (path + file_list[i * div + j], i, j)) for j in range(div)]
    for i in range(div)
]
pool.close()
for row in procs:
    for proc in row:
        blend, box = proc.get()
        base.paste(blend, box)
pool.join()

base.save('result.jpg', 'jpeg')
