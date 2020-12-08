==================================================
AST tree for pg_sel.py
==================================================
Module(body=[
    Import(names=[
        alias(name='pandas', asname='pd'),
      ], lineno=2, col_offset=0, end_lineno=2, end_col_offset=19),
    Import(names=[
        alias(name='psycopg2', asname=None),
      ], lineno=3, col_offset=0, end_lineno=3, end_col_offset=15),
    Assign(targets=[
        Name(id='conn', ctx=Store(), lineno=5, col_offset=0, end_lineno=5, end_col_offset=4),
      ], value=Call(func=Attribute(value=Name(id='psycopg2', ctx=Load(), lineno=5, col_offset=7, end_lineno=5, end_col_offset=15), attr='connect', ctx=Load(), lineno=5, col_offset=7, end_lineno=5, end_col_offset=23), args=[
        Constant(value='host=localhost dbname=tpch user=vagrant password=vagrant', kind=None, lineno=5, col_offset=24, end_lineno=5, end_col_offset=82),
      ], keywords=[], lineno=5, col_offset=7, end_lineno=5, end_col_offset=83), type_comment=None, lineno=5, col_offset=0, end_lineno=5, end_col_offset=83),
    Assign(targets=[
        Name(id='df', ctx=Store(), lineno=7, col_offset=0, end_lineno=7, end_col_offset=2),
      ], value=Call(func=Attribute(value=Name(id='pd', ctx=Load(), lineno=7, col_offset=5, end_lineno=7, end_col_offset=7), attr='read_sql_query', ctx=Load(), lineno=7, col_offset=5, end_lineno=7, end_col_offset=22), args=[
        Constant(value='SELECT * FROM CUSTOMER', kind=None, lineno=7, col_offset=23, end_lineno=7, end_col_offset=47),
        Name(id='conn', ctx=Load(), lineno=7, col_offset=49, end_lineno=7, end_col_offset=53),
      ], keywords=[], lineno=7, col_offset=5, end_lineno=7, end_col_offset=54), type_comment=None, lineno=7, col_offset=0, end_lineno=7, end_col_offset=54),
    Assign(targets=[
        Name(id='df', ctx=Store(), lineno=10, col_offset=0, end_lineno=10, end_col_offset=2),
      ], value=Subscript(value=Name(id='df', ctx=Load(), lineno=10, col_offset=5, end_lineno=10, end_col_offset=7), slice=Index(value=Constant(value='c_name', kind=None, lineno=10, col_offset=8, end_lineno=10, end_col_offset=16)), ctx=Load(), lineno=10, col_offset=5, end_lineno=10, end_col_offset=17), type_comment=None, lineno=10, col_offset=0, end_lineno=10, end_col_offset=17),
    Assign(targets=[
        Name(id='asn', ctx=Store(), lineno=11, col_offset=0, end_lineno=11, end_col_offset=3),
      ], value=Constant(value=3, kind=None, lineno=11, col_offset=6, end_lineno=11, end_col_offset=7), type_comment=None, lineno=11, col_offset=0, end_lineno=11, end_col_offset=7),
    Assign(targets=[
        Name(id='ans2', ctx=Store(), lineno=12, col_offset=0, end_lineno=12, end_col_offset=4),
      ], value=Name(id='asn', ctx=Load(), lineno=12, col_offset=7, end_lineno=12, end_col_offset=10), type_comment=None, lineno=12, col_offset=0, end_lineno=12, end_col_offset=10),
    Assign(targets=[
        Name(id='ans3', ctx=Store(), lineno=13, col_offset=0, end_lineno=13, end_col_offset=4),
      ], value=BinOp(left=Constant(value=3, kind=None, lineno=13, col_offset=7, end_lineno=13, end_col_offset=8), op=Add(), right=Constant(value=5, kind=None, lineno=13, col_offset=9, end_lineno=13, end_col_offset=10), lineno=13, col_offset=7, end_lineno=13, end_col_offset=10), type_comment=None, lineno=13, col_offset=0, end_lineno=13, end_col_offset=10),
    Expr(value=Call(func=Name(id='print', ctx=Load(), lineno=15, col_offset=0, end_lineno=15, end_col_offset=5), args=[
        Name(id='df', ctx=Load(), lineno=15, col_offset=7, end_lineno=15, end_col_offset=9),
      ], keywords=[], lineno=15, col_offset=0, end_lineno=15, end_col_offset=10), lineno=15, col_offset=0, end_lineno=15, end_col_offset=10),
  ], type_ignores=[])

