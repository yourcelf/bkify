#!/usr/bin/env python
import os
import json
import shutil
import urllib2
import argparse
import tempfile
import subprocess

def unpack(gif, args, tmpdir):
    proc = subprocess.Popen([
        "convert", "+adjoin", "-coalesce", "-",
        os.path.join(tmpdir, "frame%02d.gif")
    ], stdin=subprocess.PIPE)
    proc.communicate(gif)

    frames = [os.path.join(tmpdir, f) for f in sorted(os.listdir(tmpdir))]
    return frames

def compose(frames, args):
    margin = args.dpi * args.margin
    imagesize = args.dpi * args.size
    paperw, paperh = (float(f) * args.dpi for f in args.papersize.split("x"))
    left_margin = (paperw - imagesize - margin) * 72. / args.dpi
    bottom_margin = (paperh - imagesize) * 72. / args.dpi / 2.
    subprocess.check_call([
        "convert", "-adjoin",
        "-density", str(args.dpi),
        "-filter", "Box",
        "-resize", "{0}x{0}".format(args.dpi * args.size),
        "-page", "{0}x{1}+{2}+{3}".format(paperw, paperh, left_margin, bottom_margin),
        "-adjoin"] + frames + [args.output])

def make_flipbook(args):
    tmpdir = tempfile.mkdtemp(prefix="flpbk")
    with open(args.jsonfile) as fh:
        data = json.load(fh)
    gifs = []
    for image in data['images']:
        res = urllib2.urlopen(image)
        gifs.append(res.read())

    frames = []
    for i, gif in enumerate(gifs):
        tmp = os.path.join(tmpdir, str(i))
        os.makedirs(tmp)
        frames += unpack(gif, args, tmp)

    compose(frames, args)
    shutil.rmtree(tmpdir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make a fnlctpr flip book.")
    parser.add_argument("jsonfile", type=unicode, help='Path to JSON file for this book.')
    parser.add_argument("output", type=unicode, help='Output path (pdf)')
    parser.add_argument("--size", default=1.5, type=float,
            help="Inner width and height of panels, in inches")
    parser.add_argument("--margin", default=0.125, type=float,
            help="Outer margin around every panel, in inches")
    parser.add_argument("--papersize", default="3.5x2", type=str,
            help="Paper size, wxh in inches (e.g. 3.5x2)")
    parser.add_argument("--dpi", default=300, type=int,
            help="DPI for resulting file")
    make_flipbook(parser.parse_args())
