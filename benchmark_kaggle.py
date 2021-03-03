def get_connstr(parsetree):
    for node in parsetree.body:
        if type(node) == ast.Assign and\
        type(node.value)== ast.Call and\
        type(node.value.func)==ast.Attribute and\
        node.value.func.attr == 'connect' and\
        type(node.value.func.value)==ast.Name and\
        node.value.func.value.id=='psychopg2':
            return node.value.args[0].value
