#!/usr/bin/env python3
"""Hand the judge the finished front page.

The page is rendered by draw24.py while the entry is built and committed
here as entry.png. This script does no drawing, needs no network and never
writes into the repository: it copies that one file into the directory the
judge names (MAKEFUN_OUTPUT_DIR, or /output when unset).
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = "entry.png"


def deliver():
    source = os.path.join(HERE, IMAGE)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE)
    shutil.copyfile(source, target)
    print("delivered %s -> %s (%d bytes)"
          % (source, target, os.path.getsize(target)))


if __name__ == "__main__":
    deliver()
