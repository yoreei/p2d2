import astroid
from dataclasses import dataclass
import json
import importlib
from p2d2.infer.inference import inference


@dataclass
class Classification:
    """The output of the Classifier

    "name":str, # name of the object being defined / operated on
    "backend":str, # backend code, e.g. SQL
    "type": str, # the type of the object
    "state: dict # additional state information that will be passed to classifications that contain this node as an argument

    Example Classification cls:
    cls.name = "df1",
    cls.backend = "declarative code...",
    cls.type = "pandas.Groupby",
    cls.state = {"by":"col1"}
    """

    name: str
    backend: str
    nametype: str
    state: dict


class Classifier:
    def __init__(self, backend="SQL"):
        with open("pandas2ir.json") as json_file:
            self.mapping = json.load(json_file)
        self.backend = importlib.import_module(f"ir2{backend}")

    def classify(self, node, state) -> Classification:
        """
        Main entry point to the classifier.
        """
        node_dict = dictify(node, state)
        for function in self.mapping:
            if node_compare(node_dict, function):
                print("its a match")
                return self.compile_action(node_dict, function["action"], state)
        return None

    def compile_action(
        self, node_dict: dict, raw_action: dict, state: dict
    ) -> Classification:
        """
        Takes a dictified Call node and an action as defined by the mapping and produces valid backend code. Example:
        {
        "ir": "JOIN('another_table', 'inner', 'col1=col2', 'table')"
        "type": "pandas.DataFrame"
        """
        operand1 = node_dict["kwarg_values"]["self"]
        parameters = node_dict["kwargs_values"]
        parameters.update(state[operand1])
        ir = raw_action["ir"].format(**parameters)
        raw_action["backend"] = self.backend.compile(ir)
        del raw_action["ir"]
        return raw_action
        # result = {
        # "code": self.backend.compile(ir),
        # "type": raw_action["type"],
        # "state": raw
        # }


def node_compare(node_dict: dict, function: dict) -> bool:
    """
    Compares a dictified node and the "req" part of a mapping.
    Example:
    """
    return node_dict == function["req"]


def get_type(node, state):
    """handles 2 cases:
    1. Node is a const
    2. Node is a name constained in state
    """
    # could also try pytype()
    try_const = node.inferred()[0].qname()
    if try_const == astroid.Uninferable:
        return state[node.name]["type"]
    else:
        return try_const


def get_value(name_or_const):
    """
    return the constant value of a variable. Works only for elementary types, e.g. int, str, list
    Example:
    val = 2
    call(arg1 = dataframe, arg2 = val, arg3 = "inner")

    this function would return:
    for arg | returns
    --------| -------
    arg1    | None
    arg2    | 2
    arg3    | "inner"
    """
    inferred_type = name_or_const.inferred()[0]
    isinstance_partial = lambda x: isinstance(inferred_type, x)
    possible_types = [astroid.Const, astroid.List]
    if any(map(isinstance_partial, possible_types)):
        # type.value works only for Const. as_string with eval works
        # for containers too
        return eval(inferred_type.as_string())
    else:
        return None


def get_varname(name_or_const):
    """
    Example:
    val = 2
    call(arg1 = dataframe, arg2 = val, arg3 = "inner")

    this function would return:
    for arg | returns
    --------| -------
    arg1    | "dataframe"
    arg2    | "val"
    arg3    | ""
    """
    if isinstance(name_or_const, astroid.Name):
        return name_or_const.name
    else:
        return ""


def dictify(node, state):
    """
    Example:
    ```
    pandas.read_sql_table(table_name = "table", con=connector, columns=["col1"])
    ```
    {
    "attrname": "read_sql_table",
    "self_type": "pandas",
    "kwargs_values": {"table_name": "", "con" = "", columns=["col1"]},
    "kwargs_types": {"table_name": "str", "con" = "psycopg2.Connectible", columns="list"}
    "kwargs_varnames": {"table_name": "df", "con" = "conn", columns=""}
    }
    ```

    """

    dict_form = {}
    """qname could be:
    'pandas.core.frame.DataFrame' for the dataframe or
    'pandas' for the module
    TODO why .core.frame?????
    """
    dict_form["attrname"] = node.func.attrname  # "read_sql_table"
    if hasattr(node.func, "expr"):
        dict_form["self_type"] = get_type(node.func.expr, state)
    else:
        # it's a global function
        dict_form["self_type"] = ""
    dict_form["kwargs_types"] = {}
    dict_form["kwargs_values"] = {}
    dict_form["kwargs_varnames"] = {}

    # node.keywords may be None
    keywords = node.keywords if node.keywords else []
    for keyword in keywords:
        uid = keyword.arg  # e.g. table_name
        dict_form["kwargs_types"][uid] = get_type(keyword.value, state)
        dict_form["kwargs_values"][uid] = get_value(keyword.value)
        dict_form["kwargs_varnames"][uid] = get_varname(keyword.value)
    print("why .core.frame?????")
    print(dict_form)

    return dict_form
