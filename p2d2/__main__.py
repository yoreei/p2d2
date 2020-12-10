#!/usr/bin/env python3
import ast
import _ast

#import grizzly
#import sqlite3

import argparse_factory
import nodes
import astpp

class Ast2pr(ast.NodeTransformer):

    def visit_Assign(self, node):
#        return ast.copy_location(ast.Subscript(
#            value=ast.Name(id='data', ctx=ast.Load()),
#            slice=ast.Index(value=ast.Str(s=node.id)),
#            ctx=node.ctx
#        ), node)
        try:
            if node.value.func.attr == 'read_sql_query':
                dtable_query = node.value.args[0].value # 'SELECT * FROM customer'
                dtable_conn = node.value.args[1].id # 'conn'
                dtable_src = dtable_query.split()[-1] # 'customer'
                dtable_orig = node
                dbtable = nodes.DBTable(dtable_conn, dtable_src, dtable_orig)

                tar=node.targets[0].id 
                src = dbtable
                inPlace = False # because rel. table -> variable
                orig = node
                p2b2_assign = nodes.P2B2_Assign(tar, inPlace, src, orig) 
                return p2b2_assign 
        except (AttributeError):

            pass
  #      print('here')
  #      breakpoint()
        try:
 
            if type(node.value)==_ast.Subscript and \
type(node.value.value)==_ast.Attribute and \
                node.value.value.attr=='loc' and \
                type(node.value.slice.dims[0])==_ast.Slice and \
                node.value.slice.dims[0].lower == node.value.slice.dims[0].upper == \
                node.value.slice.dims[0].step == None and \
                type(node.value.slice.dims[1]) == _ast.Index:
                    if type(node.value.slice.dims[1].value)==_ast.List:
                        cols=[]
                        for el in node.value.slice.dims[1].value.elts:
                            cols += [el.value]
                        
                        src = node.value.value.value.id
                        proj = nodes.Projection(cols,src,node)
                        
                        tar = node.targets[0].id
                        inPlace = tar == src
                        return nodes.P2B2Assign(tar,inPlace,proj,node)
        except (AttributeError):
            return node
                     
            



#    Assign(targets=[
#        Name(id='a', ctx=Store(), lineno=9, col_offset=0, end_lineno=9, end_col_offset=1),
#      ], value=Call(func=Attribute(value=Name(id='pd', ctx=Load(), lineno=9, col_offset=4, end_lineno=9, end_col_offset=6), attr='read_sql_query', ctx=Load(), lineno=9, col_offset=4, end_lineno=9, end_col_offset=21), args=[
#        Constant(value='SELECT * FROM customer', kind=None, lineno=9, col_offset=22, end_lineno=9, end_col_offset=46),
#        Name(id='conn', ctx=Load(), lineno=9, col_offset=48, end_lineno=9, end_col_offset=52),
#      ], keywords=[], lineno=9, col_offset=4, end_lineno=9, end_col_offset=53), type_comment=None, lineno=9, col_offset=0, end_lineno=9, end_col_offset=53),

def main():
    args = argparse_factory.parse_args()
    with open(args.filepath, "r") as source:
        analyze(source)

#def transform(source: str):
#    ir = code2ir(source)
#    bytecode = ir2bytecode(ir)
#    write_bytecode(bytecode)
#
#    tree = ast.parse(source.read())
#
#    analyzer = Analyzer()
#    analyzer.visit(tree)
#    analyzer.report()

def code2pr(code=None):
    code ="""
a = pd.read_sql_query('SELECT * FROM customer', conn)
b = a.loc[:,['c_custkey','c_name','c_acctbal']] # we assume a projection is always a copy
machineLearningAlgorithm(b)
"""
    codetree = ast.parse(code)

    return Ast2pr().visit(codetree)

def code2imr(code):
    pr = code2pr(code)
    

def code2opR(code):
    imr = code2imr(code)

def code2bytecode(code):
    pass

def write_bytecode(bytecode):
    pass


#class Analyzer(ast.NodeVisitor):
#    def __init__(self):
#        self.stats = {"import": [], "from": []}
#
#    def visit_Import(self, node):
#        for alias in node.names:
#            self.stats["import"].append(alias.name)
#        self.generic_visit(node)
#
#    def visit_ImportFrom(self, node):
#        for alias in node.names:
#            self.stats["from"].append(alias.name)
#        self.generic_visit(node)
#
#    def visit_FunctionDef(self, node):
#        print(node.name)
#        self.generic_visit(node)
#
#    def report(self):
#        pprint(self.stats)


#if __name__ == "__main__":
#    main()
