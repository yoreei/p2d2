import astroid

def slices_to_getitem_transform(node):
    
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

def all():
    astroid.MANAGER.register_transform(
        astroid.Subscript,
        slices_to_getitem_transform,
    )
