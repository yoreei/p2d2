python3 -m pylint p2d2 -j 8 -d C,R,W &&
python3 -m pylint test -j 8 -d C,R,W &&
python3 -m unittest
# python3 -m unittest --failfast
