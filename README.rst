Bkify
=====

Create books from pxlshp.com images, like `this <http://unterbahn.com/2013/01/i-printed-a-pxlshp-book-of-famous-artworks/>`_.

Depends on imagemagick (``convert`` and ``montage`` must be in your path).

Example::

    ./bkify.py example.json out.pdf

Result: `out.pdf <https://raw.github.com/yourcelf/bkify/master/out.pdf`

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
