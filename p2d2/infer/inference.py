import astroid
import pandas

def inference():
    dataframe_interface()
    fix_comparison()

def dataframe_interface():
    with open('/vagrant/p2d2/infer/dataframe.pyi') as interface_file:
        interface_parsed = astroid.parse(interface_file.read())
    astroid.register_module_extender(astroid.MANAGER, "pandas", lambda x=interface_parsed: x)

def fix_comparison():
    """
    The reason we need this fix is because astroid does not create inference functions for astroid.Compare nodes by default. Even something as simple as "1<2" would result in "Uninferable". This fix adds inference capabilities for all Compare nodes that have a DataFrame object on the "left" attribute. E.g:
    
    ```
    import pandas as pd
    d = pd.DataFrame()
    m = d < 1
    ```

    Without this fix, the mask "m" would be Uninferable.

    """

    def pandas_compare(node, context=None):
        # Do some transformation here
        inferred = node.left.inferred()[0]
        return iter((inferred,))


    def predicate(node):
        inferred = node.left.inferred()[0]
        if  inferred.pytype() == "pandas.DataFrame":
            # print('yes')
            return True
        else:
            # print('no')
            return False


    # print('ho')
    astroid.MANAGER.register_transform(
        astroid.nodes.Compare,
        # For some reason raise_on_overwrite=True breaks unittests
        astroid.inference_tip(pandas_compare, raise_on_overwrite=False),
        predicate,
    )

if __name__=="__main__":
    code="""import pandas as pd
d=pd.DataFrame()
m=d<1
"""
    inference()
    p=astroid.parse(code)
    print(p.body[2].value.inferred())
    breakpoint()

