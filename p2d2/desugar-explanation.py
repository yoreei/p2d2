"""
This script is to be run to check how different grammar is represented by the AST. It's helpful when writing Python desugarizers.
"""
import astroid
from redbaron import RedBaron
subscript_lookup_code = """
class SubscriptLookup:
    def __getitem__(*args, **kwargs):
        print(f"__getitem__({args})")
a = SubscriptLookup()

"""

def astroid_lookup(code):
    parsed = astroid.parse(code)
    print(code)
    print(parsed.repr_tree())
    exec(subscript_lookup_code+code)

def redbaron_lookup(code):
    red = RedBaron(code)
    red.help(deep=True)

variants = ["a[1]",
"a['hello']",
"a[1,2]",
"a[1,'hello',2]",
"a[1:2:3]",
"a[::]",
"a[:1]",
"a[::'world']",
"a[::,1]",
"a[::,1,2]",
"a[0:1:2,3,4]"]

print("-----astroid------:\n\n")
for code in variants:
    astroid_lookup(code)

print("-----redbaron------:\n\n")
for code in variants:
    redbaron_lookup(code)
