import subprocess
from pathlib import Path

import os
from chardet import detect

# get file encoding type
def get_encoding_type(file):
    with open(file, "rb") as f:
        rawdata = f.read()
    return detect(rawdata)["encoding"]


def to_utf8(srcpath: Path, utf8_path):
    from_codec = get_encoding_type(srcpath)
    # Python 3.9 use with_stem
    trgpath = srcpath.with_name(srcpath.stem + "-utf8.ipynb")

    try:
        with open(srcpath, "r", encoding=from_codec) as srcfile:
            text = srcfile.read()  # for big files use chunks
    except UnicodeDecodeError:
        print(f"{srcpath=} Decode Error")
        return False

    try:
        with open(trgpath, "w", encoding="utf-8") as trgfile:
            trgfile.write(text)
    except UnicodeEncodeError:
        print(f"{srcpath=} Encode Error")
        return False

    return True


def all_to_utf8(sample_path: Path, utf8_path):
    successes = 0
    files = 0
    for ipynb in sample_path.glob("**/*.ipynb"):
        files += 1
        stem = str(ipynb.stem)
        if "-utf8" not in ipynb.stem:
            success = to_utf8(ipynb, utf8_path)
            if success:
                successes += 1

    print(f"{files=}")
    print(f"{successes=}")



if __name__ == "__main__":
    import sys
    
    kernels_path = Path("G:/bachelor/bigsample")
    utf8_path = Path("G:/bachelor/utf8")
    all_to_utf8(kernels_path, utf8_path)
