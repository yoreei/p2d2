import pandas

def new_report():
    return {'df':[], 'type': [], 'numcols':[], 'numrows':[], 'cols':[]}
def global_report():
    report = new_report()
    for name, obj in globals():
        report_add(report, name, obj)

    return report


def report_add(report, name, obj):
    if isinstance(obj, pandas.DataFrame):
        report['df'].append(name)
        report['type'].append('DataFrame')
        report['numcols'].append(len(obj.columns))
        report['numrows'].append(len(obj))
        report['cols'].append(list(obj.columns))
    if isinstance(obj, pandas.Series):
        report['df'].append(name)
        report['type'].append('Series')
        report['numcols'].append(1)
        report['numrows'].append(len(obj))
        report['cols'].append(list(obj.name))
        
def drop2select(df):
    cols = list(df.columns)
    sql_list = []
    for col in cols:
        sql_list.append(f'"{col}"')
    return ', '.join(sql_list)