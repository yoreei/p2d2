#!/usr/bin/env python3
import ast
import _ast

#import grizzly
#import sqlite3

from . import argparse_factory
from . import nodes
from . import astpp

class Ast2pr(ast.NodeTransformer):
    ids = [] # saves var names for Sink detection

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
                Ast2pr.ids +=[tar]
                src = dbtable
                inPlace = False # because rel. table -> variable
                orig = node
                p2d2_assign = nodes.P2D2_Assign(tar, inPlace, src, orig) 
                return p2d2_assign 
        except (AttributeError):

            pass
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
                        Ast2pr.ids += [tar]
                        inPlace = tar == src
                        return nodes.P2D2_Assign(tar,inPlace,proj,node)
        except AttributeError as e:
            print(e)
            return node
        
#        if is_action(node):
def iter_ids(tree):
#TODO with getattr()
    for node in tree.body:
        if type(node)==nodes.P2D2_Assign:
            yield node.tar

def wrap_actions(tree):

    for count in range(0,len(tree.body)):
        topnode = tree.body[count]
        if not isinstance(topnode, nodes.P2D2_Node):
            for child in ast.walk(topnode):
                if type(child)==ast.Name and child.id in iter_ids(tree):
                    action = nodes.Action(child.id, topnode)
                    tree.body[count] = action
def insert_pulls(tree):
    """
    Works in-place
    """
    for count in reversed(range(len(tree.body))):
        if type(tree.body[count]) == nodes.Action:
            tar = tree.body[count].src.name
            src = tree.body[count].src.name
            tree.body.insert(count, nodes.Pull(tar, src, None))
            
                    
    
def main():
    args = argparse_factory.parse_args()
    with open(args.filepath, "r") as source:
        analyze(source)

def lp(*trees, dump=astpp.dump):
    """long print"""
    breakpoint()
    for tree in trees:
        print(dump(tree))
        print('\n-------\n')
def sp(*trees):
    def _short_print(tree):
        return tree.body
    for tree in trees:
        for el in tree.body:
            print(type(el).__name__)

def code2pr(code):
    """
    Converts a code string to Procedural Representation (#1 ir). There are 2 substages to achieving PR:
    1. Wrap supported operations
    2. Wrap actions (depends on completion of 1.)
    """
    codetree = ast.parse(code)
    pr= Ast2pr().visit(codetree)
    wrap_actions(pr)
    insert_pulls(pr)
    return pr

def code2imr(code=None):
    """
    """

    code ="""
a = pd.read_sql_query('SELECT * FROM customer', conn)
b = a.loc[:,['c_custkey','c_nationkey','c_acctbal']] # we assume a projection is always a copy
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
machineLearningAlgorithm(b)
print(a)
print(b)
ignoreme()
    """
    def name_update(body, name):
        def up_src(node, name):
            src = getattr(node, 'src', None)

            if type(src) == nodes.NameStep:
                if src.name == name:
                    src.count+=1
            else:
                up_src(node.src, name)

        def up_tar(node, name):
            #not all of our nodes have a tar
            if getattr(node, 'tar', None) == name:
                node.tar.count+=1

        for node in body:
            if isinstance(node, nodes.P2D2_Node):
                up_src(node, name)
                up_tar(node, name)
        
    pr = code2pr(code)
    namecount={}
    for i in range(0,len(pr.body)):
        node = pr.body[i]
        if getattr(node, 'inPlace', False):
            node.tar.count+=1
            name_update(pr.body[i+1:], node.tar.name)
    
    imr=pr
    breakpoint()
    return imr            
    
    

def code2opR(code=None):
    code ="""
a = pd.read_sql_query('SELECT * FROM customer', conn)
b = a.loc[:,['c_custkey','c_nationkey','c_acctbal']] # we assume a projection is always a copy
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
machineLearningAlgorithm(b)
print(a)
print(b)
ignoreme()
    """
#    def isoptimized(node):
#        if getrootattr(node)==nodes.DBTable:
#            return True
#        else:
#            return False
#    def optimize(body, node):
#        if isoptimized(node):
#            return node
#        else:
#            getrootattr(node, 'src')=findbytar(body,  

    def getrootattr(node, attr):
        """
        Follows the attribute and the attribute's attribute, etc. until a node no longer has the specified attribute. Then, return the node
        """
        if not hasattr(node, attr):
            return node
        else:
            return getrootattr(getattr(node, attr), attr)   
    def setrootattr(node, attr):
        pass
        #TODO
        
    def findbytar(body, tar:nodes.NameStep):
        for node in body:
            if getattr(node, 'tar', None).__repr__() == tar.__repr__():
                return node 


    def build_pipeline(body, node):
        print('build_pipeline on node', node)
        if type(getrootattr(node, 'src')) == nodes.DBTable:
            return
        else:
            root = getrootattr(node, 'src')
            root = findbytar(body, getrootattr(node, 'src'))
            breakpoint()
            return build_pipeline(body, node)
        
    imr = code2imr(code)
    
    for node in imr.body:
        print('main loop on node:', node)
        if type(node)==nodes.Pull:
            build_pipeline(imr.body, node) 

    opr=imr
    breakpoint()
    return opr

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

#def wrap_src(body):
#    def _drill_down(node, attr_name):
#        attr = getattr(node, attr_name, None)
#
#        if type(attr) == str:
#            setattr(node, attr_name, NameStep(attr)
#        elif hasattr(attr, attr_name):
#            _drill_down(attr, attr_name)
#
#    for node in body:
#        _drill_down(node)


#class NameDict(dict):
#    def stepname(self, name:str):
#        return name+'_p2d2_'+str(self.get(name, 1))

if __name__ == "__main__":
    #code2opR()
    code2imr()
#    main()
