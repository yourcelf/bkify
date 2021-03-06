#!/usr/bin/env python
import re
import os
import json
import base64
import shutil
import tempfile
import argparse
import subprocess

def image_panel(data, args, dest, opts=None):
    b64data = re.sub("^data:image/png;base64,", "", data['data'])
    img = base64.b64decode(b64data)
    args = ["convert", "-",
            "-filter", "Box",
            "-resize", "{0}x{0}".format(args.size * args.dpi)

        ] + (opts or []) + [dest]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate(img)
    return dest

def title_panel(data, args, dest, opts=None):
    args = ["convert", "-background", "white", "-size", "{0}x{0}".format(args.dpi * args.size),
            "-fill", "black", "-font", args.font,
            "-pointsize", str(int(args.dpi * args.size / 8)),
            "-gravity", "West",
            u"caption:{0}\n\n{1}".format(data['title'], data['artist'])
        ]  + (opts or []) + [dest]
    subprocess.check_call(args)
    return dest

def compose(pages, args, top_name, bottom_name, combined_name):
    top = pages[0:len(pages)/2]
    bottom = pages[len(pages)/2:]
    margin = int(args.margin * args.dpi)
    cmd = ["montage", "-mode", "Concatenate", "-background", "white",
            "-tile", "x1", "-geometry", "+{0}+{0}".format(margin)]
    for imgs, name in ((top, top_name), (bottom, bottom_name)):
        subprocess.check_call(cmd + imgs + [name])
    subprocess.check_call(["convert", top_name, "-rotate", "180", top_name])
    # Add 1 px for dashed line on exterior.
    subprocess.check_call(["montage",
        top_name, bottom_name, "-mode", "Concatenate", "-tile", "1x",
        "-geometry", "+1+1", combined_name])
    unit = (args.size + args.margin*2) * args.dpi
    height = unit * 2 + 2
    width = (unit - 1) * len(pages) / 2 + 2
    dash = args.dpi / 30
    # Draw lines
    subprocess.check_call(["convert", combined_name,
        "-stroke", "black", "-fill", "white",
        # Middle
        "-draw", "stroke-dasharray {0} {0} path 'M {1},{2} L {3},{4}'".format(
            dash, unit + 1, height/2, width - unit - 1, height/2
        ),
        # Top
        "-draw", "stroke-dasharray {0} {0} path 'M {1},{2} L {3},{4}'".format(
            dash, 0, 0, width, 0
        ),
        # Bottom
        "-draw", "stroke-dasharray {0} {0} path 'M {1},{2} L {3},{4}'".format(
            dash, 0, height - 1, width, height - 1
        ),
        # Left
        "-draw", "stroke-dasharray {0} {0} path 'M {1},{2} L {3},{4}'".format(
            dash, 1, 0, 1, height
        ),
        # right
        "-draw", "stroke-dasharray {0} {0} path 'M {1},{2} L {3},{4}'".format(
            dash, width - 1, 0, width - 1, height
        ),
        "-density", str(args.dpi), args.output])
    return args.output

def make_book(args):
    with open(args.jsonfile) as fh:
        data = json.load(fh)

    tmp = tempfile.mkdtemp(prefix="bkify")
    tmp_name = lambda n: os.path.join(tmp, n)

    pages = [
        image_panel(data['front'], args, tmp_name("front.png")),
    ]
    for i,img in enumerate(data['images']):
        pages.append(image_panel(img, args, tmp_name("{0}-image.png".format(i))))
        pages.append(title_panel(img, args, tmp_name("{0}-title.png".format(i))))
    pages.append(image_panel(data['back'], args, tmp_name("back.png")))
    compose(pages, args, tmp_name("top.png"), tmp_name("bottom.png"), tmp_name("combined.png"))
    shutil.rmtree(tmp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make a pxlshp book.")
    parser.add_argument("jsonfile", type=unicode, help='Path to the JSON file for this book.')
    parser.add_argument("output", type=unicode, help='Output path')
    parser.add_argument("--size", default=1.375, type=float,
            help="Inner width and height of panels, in inches")
    parser.add_argument("--margin", default=0.0625, type=float,
            help="Outer margin around every panel, in inches")
    parser.add_argument("--dpi", default=300, type=int,
            help="DPI for resulting file")
    parser.add_argument("--font", default="Andale-Mono-Regular", type=unicode,
            help="Font face to use. `convert -list font` to list available fonts.")
    args = parser.parse_args()
    make_book(args)

