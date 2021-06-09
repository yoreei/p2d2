import astroid
from .classifier import Classifier
from .classifier import Classification
def lazify(ast:astroid.Module) -> set:
    """
    Read the input program and prepare VIEWs, but no PULLs.
    Modifies the input variable in-place and returns a list of names that can be PULLed.
    """
    classifier = Classifier()
    state = {}
    lineno = 0
    while lineno < len(ast.body):
        line = ast.body[lineno]
        classification:Classification = classifier.classify(line, state)
        if classification:
            del ast.body[lineno]
            state[classification.name] = classification
            lazy_node = gen_lazy_node(classification.backend)
            ast.last_p2d2_node += 1
            ast.body.insert(ast.last_p2d2_node, lazy_node)
        lineno += 1
            
    return set(state) # only the keys
    
def eagerfy(ast:astroid.Module, eagerfiable:set) -> None:
    """
    inserts PULL nodes in ast
    """
    names_gen = ast.nodes_of_class(astroid.Name)
    names_in_ast = {name.name for name in names_gen}
    to_eagerfy = names_in_ast & eagerfiable
    for view in to_eagerfy:
        pull_node = gen_eager_node(view)
        ast.last_p2d2_node += 1
        ast.body.insert(ast.last_p2d2_node, pull_node)

def get_line_name(line:astroid.Expr)->str:
    """
    Handles 2 cases:
    1. Expr is an Assignment -> return target
    2. Expr is not an Assignment -> return 
    """
    return str

def gen_lazy_node(backend_code:str)->astroid.Expr:
    """
    returns a Call node (wrapped in an Expr) corresponding to this line of code:
    cur.execute("SQL..")
    """
    return astroid.parse(f"cur.execute({backend_code})").body[0]

def gen_eager_node(table_name:str)->astroid.Expr:
    """
    returns a Call node (wrapped in an Expr) corresponding to this line of code:
    pandas.read_sql_table(table_name= table_name, con=conn)
    """
    return astroid.parse(f"pandas.read_sql_table(table_name= {table_name}, con=conn)").body[0]
