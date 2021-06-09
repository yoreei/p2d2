"""
What this module does by examples: 

a[1:2:3] -> a.__getitem__(slice(1,2,3))
a[::] -> a.__getitem__(slice(None, None, None))
a[:1] -> a.__getitem__(slice(None, 1, None))
a[::'world'] -> a.__getitem__(slice(None, None, 'world'))

a[3] -> a.__getitem__(3)
a['hello world'] -> a.__getitem__('hello world')

Not implemented:
a,b = 1 -> a = 1; b = a
"""

from redbaron import RedBaron
from redbaron import nodes

def tuplize(params):
    """
    params: could be TupleNode, AtomtrailersNode, etc

    __getitem__ always received only one input parameter.
    If more than one parameters are passed to the subscript,
    e.g. a[1,2] then they are enclosed in a tuple:
    a.__getitem__((1,2))

    This function performs this encapsulation IF NECESSARY
    """
    if isinstance(params, nodes.TupleNode) and len(params) > 1:
        return "("+params.dumps()+")"
    else:
        return params.dumps()
        

def unslice(red):
    for slice_node in red("slice"):
        lower = slice_node.lower
        upper = slice_node.upper
        step = slice_node.step
        slice_node.replace(f"slice({lower},{upper},{step})")

def unsubscript(red):
    for subscript_node in red("getitem"):
        # subscript_node => [slice(0,1,2),3]
        subscript_params= subscript_node.value #  => TupleNode: slice(0,1,2),3
        params_string = tuplize(subscript_params)
        idx = subscript_node.index_on_parent
        dotproxy = subscript_node.parent.value
        name, call = RedBaron(f"__getitem__({params_string})")[0]
        dotproxy[idx]=name.dumps()
        dotproxy.insert(idx+1, call.dumps())

def single_target(red):
    """
    NOT IMPLEMENTED
    Example:
    a, b = 1 -> a = 1; b = a
    """
    pass

def desugar(code):
    red = RedBaron(code)
    unslice(red)
    unsubscript(red)
    single_target(red)
    return red.dumps()

if __name__=="__main__":
    pass
    #desugar()
