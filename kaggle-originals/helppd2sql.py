import pandas

def new_report():
    return {'df':[], 'type': [], 'numcols':[], 'numrows':[], 'cols':[]}
def global_report(env):
    report = new_report()
    for name, obj in env.items():
        report_add(report, name, obj)
        print(f'{len(report["df"])=}')

    return report


def report_add(report, name, obj):
    if isinstance(obj, pandas.DataFrame):
        print(f'found df {name}')
        report['df'].append(name)
        report['type'].append('DataFrame')
        report['numcols'].append(len(obj.columns))
        report['numrows'].append(len(obj))
        report['cols'].append(list(obj.columns))
    elif isinstance(obj, pandas.Series) or isinstance(obj, pandas.Index):
        print(f'found series {name}')
        report['df'].append(name)
        report['type'].append('Series')
        report['numcols'].append(1)
        report['numrows'].append(len(obj))
        report['cols'].append([obj.name])
    else:
        print(f"not counted in report: {type(obj)=}")
        
def drop2select(df):
    cols = list(df.columns)
    sql_list = []
    for col in cols:
        sql_list.append(f'"{col}"')
    return ', '.join(sql_list)
