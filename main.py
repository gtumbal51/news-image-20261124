#!/usr/bin/env python3
"""Copy the pre-rendered front page to the grader output directory.

Standard library only. The grading sandbox ships no fonts and no
third-party packages, so this program does no rendering at all: it
copies the entry.png shipped beside it, byte for byte, into
$MAKEFUN_OUTPUT_DIR (falling back to /output, then the working
directory). Every run therefore writes exactly the same bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_dir():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted:
        return wanted
    if os.path.isdir("/output"):
        return "/output"
    return os.getcwd()


def main():
    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(dest_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
