import subprocess
from pathlib import Path

import os
from chardet import detect

# get file encoding type
def get_encoding_type(file):
    with open(file, "rb") as f:
        rawdata = f.read()
    return detect(rawdata)["encoding"]


def to_utf8(srcpath: Path):
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


def all_to_utf8(sample_path: Path):
    result = True
    for ipynb in sample_path.glob("**/*.ipynb"):
        stem = str(ipynb.stem)
        if "-utf8" not in ipynb.stem:
            result = result and to_utf8(ipynb)
    return result


def all_to_py(sample_path):

    successful = 0
    total = 0
    for ipynb in sample_path.glob("**/*.ipynb"):
        process = subprocess.run(
            ["jupyter", "nbconvert", "--to", "script", ipynb.as_posix()],
            capture_output=True,
        )
        print(f"{process.stdout=}\n{process.stderr=}")
        successful = successful + 1 if process.returncode == 0 else successful
        total += 1
    print(f"{total=}, {successful=}")

    return True


if __name__ == "__main__":
    import sys

    sample_path = Path(sys.argv[1])
    all_to_py(sample_path)
    # print(f'{all_to_utf8(sample_path)=}')
    # print(f'{all_to_py(sample_path)=}')
