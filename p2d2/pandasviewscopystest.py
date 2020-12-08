import pandas as pd
import io

#def tpch2dfname(tbl:str):
#    fakefile = io.StringIO(tbl)
#    return pd.read_csv(fakefile, sep='|', names=['custkey','name','address','nationkey','phone','acctbal','mktsegment','comment'])

def tpch2df(tbl:str):
    fakefile = io.StringIO(tbl)
    return pd.read_csv(fakefile, sep='|')

def df_is_view(data):
#    rows = data.iloc[1:3]
#    print (f'rows slice is view? {rows._is_view}')
#    cols = data.iloc[:,1]
#    print (f'col slice is view? {cols._is_view}')
    where = data.loc[data.loc[:,'name'].str.startswith('C')]
    print (where._is_view)
    
customer_str=tpch2df("""
custkey|name|address|nationkey|phone|acctbal|mktsegment|comment
1|Customer#000000001|IVhzIApeRb ot,c,E|15|25-989-741-2988|711.56|BUILDING|to the even, regular platelets. regular, ironic epitaphs nag e
2|Customer#000000002|XSTf4,NCwDVaWNe6tEgvwfmRchLXak|13|23-768-687-3665|121.65|AUTOMOBILE|l accounts. blithely ironic theodolites integrate boldly: caref
3|Customer#000000003|MG9kdTD2WBHm|1|11-719-748-3364|7498.12|AUTOMOBILE| deposits eat slyly ironic, even instructions. express foxes detect slyly. blithely even accounts abov
4|Customer#000000004|XxVSJsLAGtn|4|14-128-190-5944|2866.83|MACHINERY| requests. final, regular ideas sleep final accou
5|Customer#000000005|KvpyuHCplrB84WgAiGV6sYpZq7Tj|3|13-750-942-6364|794.47|HOUSEHOLD|n accounts will have to unwind. foxes cajole accor
6|Customer#000000006|sKZz0CsnMD7mp4Xd0YrBvx,LREYKUWAh yVn|20|30-114-968-4951|7638.57|AUTOMOBILE|tions. even deposits boost according to the slyly bold packages. final accounts cajole requests. furious
""")

name_address_str =tpch2df("""
name|address
Customer#000000001|IVhzIApeRb ot,c,E
Customer#000000002|XSTf4,NCwDVaWNe6t
Customer#000000003|MG9kdTD2WBHm111
Customer#000000004|XxVSJsLAGtn414-
Customer#000000005|KvpyuHCplrB84WgAi
Customer#000000006|sKZz0CsnMD7mp4Xd0
Customer#000000007|TcGe5gaZNgVePxU5k
""")
int_int =tpch2df("""
custkey|num2
1234|312
334|42
34|4312
4|4312
1234|412
""")

id_address = tpch2df("""
custkey|address
1|IVhzIApeRb ot,c,E
2|XSTf4,NCwDVaWNe6t
3|MG9kdTD2WBHm111
4|XxVSJsLAGtn414-
5|KvpyuHCplrB84WgAi
6|sKZz0CsnMD7mp4Xd0
7|TcGe5gaZNgVePxU5k
""")

#df_is_view(customer_str)
df_is_view(name_address_str)
#df_is_view(int_int)
#df_is_view(id_address)

def maskcopy():
    import pgconn
    conn = pgconn.get() #gives us a connection to PostgreSQL.
    a = pd.read_sql_query('SELECT * FROM customer', conn)
    mask = a['c_acctbal'] < 800
    c = a.loc[mask, 'c_acctbal'] #copy
    v = a.loc[:, 'c_acctbal'] #view
    vs = a.loc[:,['c_acctbal']] #view
    vv = a.loc[:, 'c_acctbal':'c_acctbal'] #view
    vi = a.iloc[:, 0:0] # copy
    v0 = a.iloc[:, 0] # view
    print (c._is_view)
    print (v._is_view)
    print (vv._is_view)
    print (vs._is_view)
    print (vi._is_view) 
    print (v0._is_view) 
