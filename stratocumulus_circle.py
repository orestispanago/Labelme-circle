import os
import glob
import json
import base64
from PIL import Image


def mkdir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def get_image_width_height(filename):
    im = Image.open(filename)
    width, height = im.size
    return width, height

def get_image_data(filename):
    with open(filename, mode='rb') as f:
        img = f.read()
    return img

def make_dict(filename):
    img = get_image_data(filename)
    width, height = get_image_width_height(filename)
    dictionary = dict(
                version = "3.16.7",
                flags= {},
                shapes = [
                    dict(
                        label = "stratocumulus",
                        line_color = None,
                        fill_color = None,
                        points = [[width/2, height/2],[height/2, 0 ]],
                        shape_type = "circle",
                        flags = {}
                        )
                    ],
                lineColor = [ 0, 255, 0, 128 ],
                fillColor = [ 255, 0, 0, 128],
                imagePath = filename,
                imageData = base64.encodebytes(img).decode('utf-8'),
                imageHeight = height,
                imageWidth = width
                )
    return dictionary

img_dir = os.path.join(os.getcwd(), "Panagopoulos-stratocumulus")
json_dir = img_dir+"-labeled"
mkdir_if_not_exists(json_dir)

images = glob.glob(f"{img_dir}/*.jpg")

for image in images:
    base_name = os.path.basename(image).split(".")[0]
    json_path = os.path.join(json_dir, base_name+".json")
    data_out = make_dict(image)
    with open(json_path, 'w') as f:
        json.dump(data_out, f, ensure_ascii=False, indent=2)
