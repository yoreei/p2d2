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
    Import(names=[
        alias(name='pgconn', asname=None),
      ], lineno=4, col_offset=0, end_lineno=4, end_col_offset=13),
    Assign(targets=[
        Name(id='conn', ctx=Store(), lineno=8, col_offset=0, end_lineno=8, end_col_offset=4),
      ], value=Call(func=Attribute(value=Name(id='pgconn', ctx=Load(), lineno=8, col_offset=7, end_lineno=8, end_col_offset=13), attr='get', ctx=Load(), lineno=8, col_offset=7, end_lineno=8, end_col_offset=17), args=[], keywords=[], lineno=8, col_offset=7, end_lineno=8, end_col_offset=19), type_comment=None, lineno=8, col_offset=0, end_lineno=8, end_col_offset=19),
    Assign(targets=[
        Name(id='a', ctx=Store(), lineno=9, col_offset=0, end_lineno=9, end_col_offset=1),
      ], value=Call(func=Attribute(value=Name(id='pd', ctx=Load(), lineno=9, col_offset=4, end_lineno=9, end_col_offset=6), attr='read_sql_query', ctx=Load(), lineno=9, col_offset=4, end_lineno=9, end_col_offset=21), args=[
        Constant(value='SELECT * FROM customer', kind=None, lineno=9, col_offset=22, end_lineno=9, end_col_offset=46),
        Name(id='conn', ctx=Load(), lineno=9, col_offset=48, end_lineno=9, end_col_offset=52),
      ], keywords=[], lineno=9, col_offset=4, end_lineno=9, end_col_offset=53), type_comment=None, lineno=9, col_offset=0, end_lineno=9, end_col_offset=53),
    Assign(targets=[
        Name(id='p', ctx=Store(), lineno=10, col_offset=0, end_lineno=10, end_col_offset=1),
      ], value=Subscript(value=Attribute(value=Name(id='a', ctx=Load(), lineno=10, col_offset=4, end_lineno=10, end_col_offset=5), attr='loc', ctx=Load(), lineno=10, col_offset=4, end_lineno=10, end_col_offset=9), slice=ExtSlice(dims=[
        Slice(lower=None, upper=None, step=None),
        Index(value=Constant(value='c_custkey', kind=None, lineno=10, col_offset=12, end_lineno=10, end_col_offset=23)),
      ]), ctx=Load(), lineno=10, col_offset=4, end_lineno=10, end_col_offset=24), type_comment=None, lineno=10, col_offset=0, end_lineno=10, end_col_offset=24),
    Assign(targets=[
        Name(id='cop', ctx=Store(), lineno=11, col_offset=0, end_lineno=11, end_col_offset=3),
      ], value=Call(func=Attribute(value=Subscript(value=Attribute(value=Name(id='a', ctx=Load(), lineno=11, col_offset=6, end_lineno=11, end_col_offset=7), attr='loc', ctx=Load(), lineno=11, col_offset=6, end_lineno=11, end_col_offset=11), slice=ExtSlice(dims=[
        Slice(lower=None, upper=None, step=None),
        Index(value=List(elts=[
            Constant(value='c_custkey', kind=None, lineno=11, col_offset=15, end_lineno=11, end_col_offset=26),
            Constant(value='c_name', kind=None, lineno=11, col_offset=27, end_lineno=11, end_col_offset=35),
            Constant(value='c_acctbal', kind=None, lineno=11, col_offset=36, end_lineno=11, end_col_offset=47),
          ], ctx=Load(), lineno=11, col_offset=14, end_lineno=11, end_col_offset=48)),
      ]), ctx=Load(), lineno=11, col_offset=6, end_lineno=11, end_col_offset=49), attr='copy', ctx=Load(), lineno=11, col_offset=6, end_lineno=11, end_col_offset=54), args=[], keywords=[], lineno=11, col_offset=6, end_lineno=11, end_col_offset=56), type_comment=None, lineno=11, col_offset=0, end_lineno=11, end_col_offset=56),
    Assign(targets=[
        Name(id='s', ctx=Store(), lineno=12, col_offset=0, end_lineno=12, end_col_offset=1),
      ], value=Subscript(value=Attribute(value=Name(id='a', ctx=Load(), lineno=12, col_offset=4, end_lineno=12, end_col_offset=5), attr='loc', ctx=Load(), lineno=12, col_offset=4, end_lineno=12, end_col_offset=9), slice=Index(value=Compare(left=Subscript(value=Attribute(value=Name(id='a', ctx=Load(), lineno=12, col_offset=10, end_lineno=12, end_col_offset=11), attr='loc', ctx=Load(), lineno=12, col_offset=10, end_lineno=12, end_col_offset=15), slice=ExtSlice(dims=[
        Slice(lower=None, upper=None, step=None),
        Index(value=Constant(value='c_acctbal', kind=None, lineno=12, col_offset=18, end_lineno=12, end_col_offset=29)),
      ]), ctx=Load(), lineno=12, col_offset=10, end_lineno=12, end_col_offset=30), ops=[
        Lt(),
      ], comparators=[
        Constant(value=800, kind=None, lineno=12, col_offset=31, end_lineno=12, end_col_offset=34),
      ], lineno=12, col_offset=10, end_lineno=12, end_col_offset=34)), ctx=Load(), lineno=12, col_offset=4, end_lineno=12, end_col_offset=35), type_comment=None, lineno=12, col_offset=0, end_lineno=12, end_col_offset=35),
    Assign(targets=[
        Subscript(value=Attribute(value=Name(id='a', ctx=Load(), lineno=13, col_offset=0, end_lineno=13, end_col_offset=1), attr='loc', ctx=Load(), lineno=13, col_offset=0, end_lineno=13, end_col_offset=5), slice=Index(value=Tuple(elts=[
            Compare(left=Subscript(value=Name(id='a', ctx=Load(), lineno=13, col_offset=6, end_lineno=13, end_col_offset=7), slice=Index(value=Constant(value='c_acctbal', kind=None, lineno=13, col_offset=8, end_lineno=13, end_col_offset=19)), ctx=Load(), lineno=13, col_offset=6, end_lineno=13, end_col_offset=20), ops=[
                Lt(),
              ], comparators=[
                Constant(value=800, kind=None, lineno=13, col_offset=23, end_lineno=13, end_col_offset=26),
              ], lineno=13, col_offset=6, end_lineno=13, end_col_offset=26),
            Constant(value='c_acctbal', kind=None, lineno=13, col_offset=28, end_lineno=13, end_col_offset=39),
          ], ctx=Load(), lineno=13, col_offset=6, end_lineno=13, end_col_offset=39)), ctx=Store(), lineno=13, col_offset=0, end_lineno=13, end_col_offset=40),
      ], value=Constant(value=4, kind=None, lineno=13, col_offset=43, end_lineno=13, end_col_offset=44), type_comment=None, lineno=13, col_offset=0, end_lineno=13, end_col_offset=44),
  ], type_ignores=[])

