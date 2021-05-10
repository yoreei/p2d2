def read_sql_table(table, conn): return DataFrame()

class DataFrame(dict):
    def head(self, num): return self
    def tail(self, num): return self
    def merge(self, df2): return self
    def __getitem__(self, key): return self
    def groupby(self, by): return GroupBy()

    def append(self, df2): return self 
    # def __missing__(self, key): pass

    def __lt__(self, *other): return self
    def __eq__(self, *other): return self
    def __le__(self, *other): return self 
    def __gt__(self, *other): return self
    def __ge__(self, *other): return self
    def __ne__(self, *other): return self
    # binary arithm operations
    def __add__(self, *other): return self
    def __sub__(self, *other): return self
    def __mul__(self, *other): return self
    def __matmul__(self, *other): return self
    def __truediv__(self, *other): return self
    def __floordiv__(self, *other): return self
    def __mod__(self, *other): return self
    def __divmod__(self, *other): return self
    def __pow__(self, *other): return self
    def __lshift__(self, *other): return self
    def __rshift__(self, *other): return self
    def __and__(self, *other): return self
    def __xor__(self, *other): return self
    def __or__(self, *other): return self

    # binary arithm. operations. Only called if left side does not support operations
    def __radd__(self, *other): return self
    def __rsub__(self, *other): return self
    def __rmul__(self, *other): return self
    def __rmatmul__(self, *other): return self
    def __rtruediv__(self, *other): return self
    def __rfloordiv__(self, *other): return self
    def __rmod__(self, *other): return self
    def __rdivmod__(self, *other): return self
    def __rpow__(self, *other): return self
    def __rlshift__(self, *other): return self
    def __rrshift__(self, *other): return self
    def __rand__(self, *other): return self
    def __rxor__(self, *other): return self
    def __ror__(self, *other): return self

    # +=, -=, etc. 
    def __iadd__(self, *other): return self
    def __isub__(self, *other): return self
    def __imul__(self, *other): return self
    def __imatmul__(self, *other): return self
    def __itruediv__(self, *other): return self
    def __ifloordiv__(self, *other): return self
    def __imod__(self, *other): return self
    def __ipow__(self, *other): return self
    def __ilshift__(self, *other): return self
    def __irshift__(self, *other): return self
    def __iand__(self, *other): return self
    def __ixor__(self, *other): return self
    def __ior__(self, *other): return self
    def __neg__(self): return self


    def __pos__(self): return self
    def __abs__(self): return self
    def __invert__(self): return self


    def __round__(self): return self
    def __trunc__(self): return self
    def __floor__(self): return self
    def __ceil__(self): return self

class GroupBy(dict):
    def max(self): return DataFrame()
    
