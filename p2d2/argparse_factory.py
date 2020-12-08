#!/usr/bin/env python3
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Optimize Python programs by performing pushdown to the underlying RDBMS")
    parser.add_argument("filepath", type=str,
                        help="path to python program to be optimized and run")
    parser.add_argument("-o", "--optimize", action="store_true",
                        help="only optimize program, without running it")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="prints the generated SQL queries")
    return parser.parse_args()
