#!/usr/bin/env python3
import ast
import _ast
import psycopg2


from . import astpp
pp = astpp.parseprint
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

def getkeyword(keywords, arg):
    for keyword in keywords:
         if keyword.arg==arg:
            value = keyword.value
    return value

class Nodedict(dict):
    def addnode(self, tar, node):
        self[tar] = self.get(tar,{})
        self[tar].update(node)

nodedict=Nodedict()

aggs = {
     'max':'MAX({0}) AS {0}',
     'mean':'AVG({0}) AS {0}',
     'min':'MIN({0}) AS {0}',
     'sum':'SUM({0}) AS {0}',
     'std':'STDDEV({0}) AS {0}',
     'var':'VARIANCE({0}) AS {0}',
     'mode':'mode() WITHIN GROUP (ORDER BY {0}) AS {0}',
     'median':'MEDIAN({0}) AS {0}',
     'sample':'RANDOM({0}) AS {0}',
}
class Ast2pr(ast.NodeTransformer):
    def is_proj(self, node):
        if type(node.value)==_ast.Subscript and \
            rgetattr(node, 'value.value.attr')=='loc' and \
            type(node.value.slice)==_ast.ExtSlice:
                return True
        return False
    
    def is_sel(self, node):
        if type(node.value)==_ast.Subscript and \
            rgetattr(node, 'value.value.attr')=='loc' and \
            type(node.value.slice)==_ast.Index and \
            type(node.value.slice.value)==_ast.Name:
                return True
        return False
    def is_mask(self,node):
        if hasattr(node.value, 'comparators'):
            return True
        return False
    def is_join(self, node):
        if type(node.value)==ast.Call and \
            type(node.value.func)==ast.Attribute and \
            node.value.func.attr=='merge':
                return True         

    def is_groupby_simple(self,node):

    def is_simple_agg(self, node):
        if type(node.value)==ast.Attribute and\
             node.value.attr=='T' and\
             type(node.value.value)==ast.Call and\
             type(node.value.value.func)==ast.Attribute and\
             node.value.value.func.attr=='to_frame' and\
             type(node.value.value.func.value)==ast.Call and\
             type(node.value.value.func.value.func) == ast.Attribute and\
             node.value.value.func.value.func.attr in aggs.keys():
                return True
        else:
            return False

    def is_mode(self, node):
        if type(node.value)==ast.Call and\
             type(node.value.func)==ast.Attribute and\
             node.value.func.attr=='head' and\
             node.value.args[0].value== 1 and\
             type(node.value.func.value)==ast.Call and\
             type(node.value.func.value.func)==ast.Attribute and\
             node.value.func.value.func.attr=='mode':
                return True 
        else:
            return False
    def is_sample(self, node):
        if type(node.value)==ast.Call and \
            type(node.value.func)==ast.Attribute and \
            node.value.func.attr=='sample' and \
            len(node.value.args)==1:
                return True
        else:
            return False

 

    def fetch_colnames(self, name, lineno):
        # unhardcode
        conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")
        cur = conn.cursor()
        src_query = resolve(name, lineno)
        cur.execute(f"create or replace temp view aggview as {src_query}")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='aggview'")
        colnames_nested = cur.fetchall() # nested like [('c_custkey'),('c_acctbal)]
        cur.close()
        conn.close()
        return [item for sublist in colnames_nested for item in sublist] # unnest like ['c_custkey'..]

    def build_aggregate_list(self, agg_type: str, colnames: list):
        aggregate_list = [] 
        for name in colnames:
            aggregate_list=aggregate_list+[aggs[agg_type].format(name)]
        return ', '.join(aggregate_list)

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
            #TODO use addnode
            nodedict[tar]={
                node.lineno:{ 
                    'sql': query,
                    'unresolved': []}}
            return
        
        if self.is_proj(node): 
        #dims = rgetattr(node, 'value.slice.dims', None)
        #proj = rgetattr(getsub(dims,1,None), 'value.elts', None)
            proj = node.value.slice.dims[1].value.elts
            cols=[e.value for e in proj]
            src = node.value.value.value.id
            tar = node.targets[0].id
            nodedict.addnode(tar, {
                node.lineno:{
                    'sql': 'SELECT '+','.join(cols)+' FROM {}',
                    'unresolved': [src]}})
            return
        
        if self.is_mask(node):
            case={
            _ast.LtE:'<=',
            _ast.Lt:'<',
            _ast.GtE:'>=',
            _ast.Gt:'>',
            _ast.Eq:'==',
            _ast.NotEq:'!='
            }
            compare_type = case[node.value.ops[0].__class__] # '<'
            col = node.value.left.slice.dims[1].value.value # 'c_custkey'
            comparator = str(node.value.comparators[0].value) # '5'
            tar = node.targets[0].id
            
            nodedict.addnode(tar,{
                node.lineno:{
                    'sql': col+compare_type+comparator,
                    'unresolved': []}})
            return
        if self.is_sel(node):
            tar = node.targets[0].id
            src = node.value.value.value.id
            maskname=node.value.slice.value.id
           
            nodedict.addnode(tar,{
                node.lineno:{
                    'sql': 'SELECT * FROM {} WHERE {{}}',
                    'unresolved': [src, maskname]}})
            return
    
        if self.is_join(node):
            tar = node.targets[0].id 
            left = node.value.func.value.id
            keywords = node.value.keywords
            right = getkeyword(keywords, 'right').id
            how = getkeyword(keywords, 'how').value
            left_on = getkeyword(keywords, 'left_on').value
            right_on = getkeyword(keywords, 'right_on').value
            
            nodedict.addnode(tar,{
                node.lineno:{
                    'sql':'SELECT * FROM {} INNER JOIN {{}} ON '+f'{left_on}={right_on};',
                    'unresolved': [left, right]}})
            return
            
        if self.is_simple_agg(node):
            tar = node.targets[0].id #maxi
            src = node.value.value.func.value.func.value.id
            agg_type = node.value.value.func.value.func.attr
            colnames = self.fetch_colnames(src, node.lineno)
            
            nodedict.addnode(tar,{
                node.lineno:{
                    'sql':'SELECT '+ self.build_aggregate_list(agg_type, colnames) + ' FROM {}',
                    'unresolved': [src]}})
            return
        
        if self.is_mode(node):
            tar = node.targets[0].id
            src = node.value.func.value.func.value.id
            agg_type = 'mode'
            colnames = self.fetch_colnames(src, node.lineno)
            
            nodedict.addnode(tar,{
                node.lineno:{
                    'sql':'SELECT '+ self.build_aggregate_list(agg_type, colnames) + ' FROM {}',
                    'unresolved': [src]}})
            return
        if self.is_sample(node):
            tar = node.targets[0].id
            src = node.value.func.value.id
            nrows = node.value.args[0].value
        
            nodedict.addnode(tar,{
                node.lineno:{
                    'sql':'select * from {} order by random() '+f'limit {nrows};',
                    'unresolved':[src]}})
            return
        
        return node
def formatsql(sql:str, put:str, alias:str):
    """
    When a query is a subquery, it needs to be enclosed in braces and given an alias, (outside of the braces, like this:

    ... FROM (SELECT * FROM CUSTOMER) AS c1
    
    The problem is that at the top level, an SQL query CANNOT be formatted as a subquery, i.e:
    
    (SELECT * FROM CUSTOMER) AS c1
    
    is an invalid SQL query if run alone like this. This function makes sure that only real subqueries are aliased.
    """
    enclosed = '('+put+f') AS {alias}'
    return sql.format(enclosed)
        
def resolve(name, callno):
    """callno is the line where the unresolved names are called, Not where they are defined"""
    defno = lastdef(name, callno)
    unresolved = nodedict[name][defno]['unresolved']
    sql = nodedict[name][defno]['sql']
    for child in unresolved:
        alias = child+'_'+str(defno)
        sql = formatsql(sql, resolve(child, defno), alias) 
    
    return sql
    
def lastdef(name, belowline):
    belowkeys=[k for k in nodedict[name].keys() if k<belowline]
    assert len(belowkeys)>0, f'can\'t find {name} below {belowline}'
    return max(belowkeys)

def requires(node):
    """Use on potential Actions to see if they depend on optimized nodes"""
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
            print(name)
            print(node.lineno)
            lastdef_lineno = lastdef(name, node.lineno)
            if (name, lastdef_lineno) in pulled: continue
            sql = resolve(name, node.lineno) 
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
    global parsetree
    parsetree = ast.parse(source)
    # removes supported nodes from parsetree in-place and populates global nodedict
    Ast2pr().visit(parsetree)
    opt_parsetree = insert_pulls(parsetree)
    breakpoint()
    return compile(opt_parsetree, 'optimized_ast', 'exec')

if __name__=='__main__':
    # This submodule is to be executed from __main__.py, this is here for interactive debugging
    with open('wflows/projsel.py', "r") as source_file:
        source = source_file.read()
    
    optimize(source) 
    
