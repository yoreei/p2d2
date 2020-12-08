#!/usr/bin/env python3
import ast

import grizzly
import sqlite3

from . import argparse_factory
import astpp

def main():
    args = argparse_factory.parse_args()
    with open(args.filepath, "r") as source:
        analyze(source)

def transform(source: str):
    ir = code2ir(source)
    bytecode = ir2bytecode(ir)
    write_bytecode(bytecode)

    tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()
def code2ir():

def ir2bytecode():
    pass

def write_bytecode(bytecode):
    pass

        dat = pd.read_sql("SELECT * FROM customer;", conn)

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


if __name__ == "__main__":
    main()
