#!/usr/bin/env python3
import ast
import _ast

from . import astpp
# https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
import functools

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

# using wonder's beautiful simplification: https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects/31174427?noredirect=1#comment86638618_31174427

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))
#-----------------------------
def getsub(subscriptable, index, default):
    """ Akin to getattr, but for subscripts. Arg `subscriptable` does not really have to be subscriptable, hence the `default` parameter"""
    try:
        subvalue = subscriptable[index]
    except TypeError: # IndexError assumes subscriptable is really subscriptable
        subvalue = default
    return subvalue

nodedict={}

def nestify_query(query:str, alias):
    """
    Makes sure that the `query` can be the subquery of another query
    """
    # nice to have: check if query already nestified
    return f'({query} AS {alias})' 

class Ast2pr(ast.NodeTransformer):

    def visit_Assign(self, node):
#        return ast.copy_location(ast.Subscript(
#            value=ast.Name(id='data', ctx=ast.Load()),
#            slice=ast.Index(value=ast.Str(s=node.id)),
#            ctx=node.ctx
#        ), node)
        if rgetattr(node, 'value.func.attr', None) == 'read_sql_query':
            tar=node.targets[0].id 
            query = node.value.args[0].value # 'SELECT * FROM customer'
            conn = node.value.args[1].id # 'conn'
            #src = dtable_query.split()[-1] # 'customer'
            nodedict[tar]={
                node.lineno:{ 
                    'sql': nestify_query(query, f'{tar}_{node.lineno}'),
                    'unresolved': None}}
            return
        
        dims = rgetattr(node, 'value.slice.dims', None)
        proj = rgetattr(getsub(dims,1,None), 'value.elts', None)
        if proj:
            cols=[e.value for e in proj]
            src = node.value.value.value.id
            tar = node.targets[0].id
            nodedict[tar] = nodedict.get(tar,{})
            nodedict[tar].update({
                node.lineno:{
                    'sql': '(SELECT '+','.join(cols)+' FROM {} AS '+f'{tar}_{node.lineno})',
                    'unresolved': src}})
            return

        return node
        
def resolve(name, lineno):
    if nodedict[name][lineno]['unresolved'] == None:
        return nodedict[name][lineno]['sql']
    else:
        unresolved = nodedict[name][lineno]['unresolved']
        return nodedict[name][lineno]['sql'].format(\
            resolve(unresolved, lastdef(unresolved, lineno)))
    
def lastdef(name, belowline):
    belowkeys=[k for k in nodedict[name].keys() if k<belowline]
    assert len(belowkeys)>0, f'can\'t find {name} below {belowline}'
    return max(belowkeys)

def requires(node):
    reqs=[]
    for child in ast.walk(node):
        if type(child)==ast.Name and child.id in nodedict.keys():
            reqs+=[child.id]
    return reqs

def gen_pullnode(name, lineno, sql):
    # Nice to have: detect correct conn and pd
    return ast.Assign(\
        targets=[ast.Name(id=name, ctx=ast.Store())],\
        value=ast.Call(\
            func=ast.Attribute(\
                value=ast.Name(id='pd', ctx=ast.Load()),\
                attr='read_sql_query', ctx=ast.Load()),\
            args=[\
                ast.Constant(value=sql, kind=None),\
                ast.Name(id='conn', ctx=ast.Load())],\
            keywords=[]),\
        type_comment=None,
        lineno=lineno)

def insert_pulls(tree):
    pulled=[]
    opt_body=[]
    for node in tree.body:
        reqs = requires(node)
        for name in reqs:
            lastdef_lineno = lastdef(name, node.lineno)
            if (name, lastdef_lineno) in pulled: continue
            sql = resolve(name, lastdef_lineno) 
            opt_body+=[gen_pullnode(name, lastdef_lineno, sql)]
            pulled+=[(name, lastdef_lineno)]

        opt_body+=[node]
    
    opt_tree = ast.Module(body=opt_body, type_ignores=[])
    
    return ast.fix_missing_locations(opt_tree) 

import marshal
import py_compile
import time

#def compile_to_file(tree):
#    # https://stackoverflow.com/questions/8627835/generate-pyc-from-python-ast
#    # make this work
#    codeobject = compile(tree, '<string>', 'exec')
#    with open('output.pyc', 'wb') as fc:
#        fc.write('\0\0\0\0')
#        py_compile.wr_long(fc, long(time.time()))
#        marshal.dump(codeobject, fc)
#        fc.flush()
#        fc.seek(0, 0)
#        fc.write(py_compile.MAGIC)

def optimize(source:str):
    parsetree = ast.parse(source)
    # removes supported nodes from parsetree in-place and populates global nodedict
    Ast2pr().visit(parsetree)
    opt_parsetree = insert_pulls(parsetree)
    # breakpoint()
    return compile(opt_parsetree, 'optimized_ast', 'exec')

if __name__=='__main__':
    # This submodule is to be executed from __main__.py, this is here for interactive debugging
    testcode="""
import pandas as pd
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=vagrant password=vagrant")

a = pd.read_sql_query('SELECT * FROM customer', conn)
b = a.loc[:,['c_custkey','c_nationkey','c_acctbal']] # we assume a projection is always a copy
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
print(b)
print(a)
print(b)
print("the end")
"""
    # populate nodedict
    optimize(testcode) 
    
    print(resolve('b', lastdef('b', 100)))
