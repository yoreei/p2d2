https://www.kaggle.com/corochann/covid-19-current-situation-in-2021

(Can be) supported:
    DataFrame.rename
    DataFrame.replace
    ~ (bitwise negation after mask)
    DataFrame.merge (on multiple cols)
    DataFrame.drop (specific case of projection)
    DataFrame.groupby().sum()
    DataFrame.fillna
    pandas.concat (like UNION ALL)
    DataFrame.unique (after single column projection)
    DataFrame.sort_values
Hard:
    Series.str.match
    pandas.melt (see explanation below)

https://www.kaggle.com/startupsci/titanic-data-science-solutions
(Can be) supported:
    DataFrame.groupby().mean()
    DataFrame.sort_values
    pandas.crosstab (see explanation below) Postgres has a crosstab func!
    drop
    fillna (a specific case of map)
    map (see explanation)
    dropna (relational selection)
Hard:
    pandas.cut


```
# melt
df
   A  B  C
0  a  1  2
1  b  3  4
2  c  5  6

pd.melt(df, id_vars=['A'], value_vars=['B', 'C'])
   A variable  value
0  a        B      1
1  b        B      3
2  c        B      5
3  a        C      2
4  b        C      4
5  c        C      6


# crosstab
>>> diamonds.head()
   carat      cut color clarity  depth  table  price     x     y     z
0   0.23    Ideal     E     SI2   61.5   55.0    326  3.95  3.98  2.43
1   0.21  Premium     E     SI1   59.8   61.0    326  3.89  3.84  2.31
2   0.23     Good     E     VS1   56.9   65.0    327  4.05  4.07  2.31
3   0.29  Premium     I     VS2   62.4   58.0    334  4.20  4.23  2.63
4   0.31     Good     J     SI2   63.3   58.0    335  4.34  4.35  2.75
>>> pd.crosstab(index=diamonds['cut'], columns=diamonds['color'])
color         D     E     F     G     H     I    J
cut
Ideal      2834  3903  3826  4884  3115  2093  896
Premium    1603  2337  2331  2924  2360  1428  808
Very Good  1513  2400  2164  2299  1824  1204  678
Good        662   933   909   871   702   522  307
Fair        163   224   312   314   303   175  119

# map

title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
dataset.map(title_mapping)
```
