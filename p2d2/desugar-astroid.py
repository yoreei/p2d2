import astroid

def slices_to_getitem_transform(node):
    def extSlice_transform(node):
        """
        WIP
        examples:
        lookup("a[::,1]")
        lookup("a[::,1,2]")
        lookup("a[0:1:2,3,4]")
        """
        getitem_call_node = astroid.Call(
                lineno=node.lineno,
                col_offset=node.col_offset,
                parent=node.parent,
            )
        tuple_node = astroid.Tuple(
                lineno=node.lineno,
                col_offset=node.col_offset,
                parent=node.getitem_call_node,
            )
        #slice_call_node = astroid.Call(
        #        lineno=node.lineno,
        #        col_offset=node.col_offset,
        #        parent=node.tuple_node,
        #    )
        #slice_call.postinit(
        #        func=attribute_node,
        #        args=[node.slice.value],
        #        keywords=None
        #    )
        
    
    def slice_transform(node):
        """
        WIP
        a[1:2:3] -> a.__getitem__(slice(1,2,3))
        a[::] -> a.__getitem__(slice(None, None, None))
        a[:1] -> a.__getitem__(slice(None, 1, None))
        a[::'world'] -> a.__getitem__(slice(None, None, 'world'))
        """
        getitem_call_node = astroid.Call(
                lineno=node.lineno,
                col_offset=node.col_offset,
                parent=node.parent,
            )
        getitem_attribute_node = astroid.Attribute(
                attrname='__getitem__',
                lineno=node.lineno,
                col_offset=node.col_offset,
                parent=getitem_call_node
            )
        #slice_attribute_node = astroid.Attribute(
        #slice_call_node = astroid.Call(
        #        lineno=node.lineno,
        #        col_offset=node.col_offset,
        #        parent=node.parent,
        #    )
        #slice_call_node.postinit(
        #        func=attribute_node,
        #        args=[node.slice.value],
        #        keywords=None
        #    )
        #attribute_node.postinit(
        #        expr=node.value
        #    )
        #call_node.postinit(
        #        func=attribute_node,
        #        args=[node.slice.value],
        #        keywords=None
        #    )

    def index_transform(node):
        """
        examples:
        a[3] -> a.__getitem__(3)
        a['hello world'] -> a.__getitem__('hello world')
        """
        call_node = astroid.Call(
                lineno=node.lineno,
                col_offset=node.col_offset,
                parent=node.parent,
            )
        attribute_node = astroid.Attribute(
                attrname='__getitem__',
                lineno=node.lineno,
                col_offset=node.col_offset,
                parent=call_node
            )
        attribute_node.postinit(
                expr=node.value,
            )
        call_node.postinit(
                func=attribute_node,
                args=[node.slice.value],
                keywords=None
            )
        return call_node
        
    if isinstance(node.slice, astroid.ExtSlice):
        return extSlice_transform(node)
    elif isinstance (node.slice, astroid.Slice):
        return slice_transform(node)
    elif isinstance(node.slice, astroid.Index):
        return index_transform(node)
    

def all():
    astroid.MANAGER.register_transform(
        astroid.Subscript,
        slices_to_getitem_transform,
    )
