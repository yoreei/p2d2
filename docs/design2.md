# Design v2

## Why start again?

Two reasons:

- The structures (read, classes) of Design v1 were aimed to completely overtake the codetree by wrapping around the original Python classes. The rationale was that the original Python classes do not provide the information that the optimizer needs while also bringing a lot of "unneeded clutter". However, during the implementation of Design v1, the classes of the optimizer started to look more and more like the stock classes they were supposed to mask - a lot of what I previously considered "clutter" started to seem useful. 

- The implementation of Design v1 made me familiar with the workings of the `ast` module - I now have my opinions of when it is advantageous to use the tools provided by the `ast` module and when it's better to "roll your own". In hindsight, the implementation of Design v1 was the opposite of optimal in this regard.

## Step 1: the creation of "nodedict"

Nodedict is supposed to store the ids of variable and the SQL which generates these variables:

```python
vardict = {
    "a" : {
        1 : {
            "sql" : "SELECT * FROM customer",
            "unresolved : None,},
        2: {
            "sql" : "SELECT c_acctbal FROM {}",
            "unresolved" : 'a',},
        },
    "b" : {
        3: {
            "sql" : "SELECT * FROM {} WHERE c_acctbal > 500",
            "unresolved" : 'a',},
        } 
}

```

Use .format to nest queries
