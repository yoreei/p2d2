def read_sql_table(table, conn): return DataFrame()

class DataFrame(dict):
    def head(self, num): return self
    def tail(self, num): return self
    def merge(self, df2): return self
    def __getitem__(self, key): return self
    def groupby(self, by): return GroupBy()

    def append(self, df2): return self 
    # def __missing__(self, key): pass
class GroupBy(dict):
    def max(self): return DataFrame()
    
