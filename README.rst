Bkify and Flpbk
===============

Create books from pxlshp.com images, like `this <http://unterbahn.com/2013/01/i-printed-a-pxlshp-book-of-famous-artworks/>`_, and make flipbooks from flnctpr.tirl.org images.

Depends on imagemagick (``convert`` and ``montage`` must be in your path).

Bkify
-----

Example::

    ./bkify.py example.json out.pdf

Result: `out.pdf <https://raw.github.com/yourcelf/bkify/master/out.pdf>`_

Options::

    usage: bkify.py [-h] [--size SIZE] [--margin MARGIN] [--dpi DPI] [--font FONT]
                    jsonfile output

    Make a pxlshp book.

    positional arguments:
      jsonfile         Path to the JSON file for this book.
      output           Output path

    optional arguments:
      -h, --help       show this help message and exit
      --size SIZE      Inner width and height of panels, in inches
      --margin MARGIN  Outer margin around every panel, in inches
      --dpi DPI        DPI for resulting file
      --font FONT      Font face to use. `convert -list font` to list available
                       fonts.

JSON file format::

    {
        "front": {
            "data": "... data URL for front cover image"
        },
        "back": {
            "data": "... data URL for back cover image"
        },
        "images": [{
            "title": "Title of image",
            "artist": "Artist of image",
            "data": "... data URL for image"
        }, ...]
    }

For best results, use an even number of images.

Flpbk
-----

Makes flipbooks out of fnlctpr.tirl.org gifs.

Example::

    ./bkify.py flip_example.json flipout.pdf

Result: `flipout.pdf <https://raw.github.com/yourcelf/bkify/master/flipout.pdf`_

Options::

    usage: flpbk.py [-h] [--size SIZE] [--margin MARGIN] [--papersize PAPERSIZE]
                    [--dpi DPI]
                    jsonfile output

    Make a fnlctpr flip book.

    positional arguments:
      jsonfile              Path to JSON file for this book.
      output                Output path (pdf)

    optional arguments:
      -h, --help            show this help message and exit
      --size SIZE           Inner width and height of panels, in inches
      --margin MARGIN       Outer margin around every panel, in inches
      --papersize PAPERSIZE
                            Paper size, wxh in inches (e.g. 3.5x2)
      --dpi DPI             DPI for resulting file

JSON file format is simple for now -- just a list of urls to gifs::

    {
        "images": [
            "url",
            "url",
            ...
         ]
    }

Each gif frame becomes a page.
