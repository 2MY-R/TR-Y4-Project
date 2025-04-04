from pathlib import Path
import shutil
import torch
from PIL import Image
import numpy as np
import imageio

def remake_dir(path):
    if path.is_dir():
        check = input(f'Delete directory {str(path)}? [y,n] ')
        if check.lower() != 'y':
            raise SystemExit(0)
        shutil.rmtree(path)
    path.mkdir(parents=True)


def min_max_scale(image):
    min = np.min(image)
    max = np.max(image)
    return (image - min) / (max - min)

def torch_min_max_scale(image):
    min = torch.min(image)
    max = torch.max(image)
    return (image - min) / (max - min)

def read_tiff(path):
    im = Image.open(path, mode='r')
    return np.array(im)

def save_tiff(array, path):
    imageio.imwrite(str(path), array)
    # im = Image.fromarray(array)
    # im.save(path)

def draw_line(array, x0, x1, y0, y1, colour):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x0, x1, y0, y1 = x0.round(), x1.round(), y0.round(), y1.round()
    print(x0, x1, y0, y1)
    transpose = abs(x1 - x0) < abs(y1 - y0)
    if transpose:
        array = torch.permute(array, (1, 0, 2))
        x0, y0, x1, y1 = y0, x0, y1, x1
    if (x0-x1).round()==0 and (y0-y1).round()==0:
        return array
    if x0 > x1:
        x0, x1, y0, y1 = x1, x0, y1, y0

    x = torch.arange(x0, x1).to(device)
    y = ((y1-y0)/(x1-x0))*(x-x0) + y0

    array[x.round().to(int), y.round().to(int), :] = colour
    return array if not transpose else torch.permute(array, (1, 0, 2))

if __name__ == '__main__':
    array = read_tiff(Path('03') / 't0000_mask.tif')
    print(np.shape(array))
    save_tiff(array, Path('03') / 't0000_mask_test.tif')
    array = read_tiff(Path('03') / 't0000_mask_test.tif')
    print(np.shape(array))

#%%
