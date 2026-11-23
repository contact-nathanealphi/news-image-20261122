"""Entry program for make.fun news-image-20261122 (Python 3.13,
standard library only).

The front page is drawn once by tools/render.py and stored as
assets/entry.png. This program only copies that file to the output
directory, so every run writes exactly the same bytes. No network,
no randomness, no timestamps.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
