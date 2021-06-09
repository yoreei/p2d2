import ast
import astunparse
import p2d2.optimizer

with open('wflowscost/proj.py', "r") as file_source:
    node = ast.parse(file_source.read())

opt=p2d2.optimizer.optimize(node, '')
breakpoint()
text=astunparse.unparse(opt)
print(text)
