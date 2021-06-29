# Backend mappings

These mappings translate from the p2d2 IR to the respective backend (PostgreSQL in this implementation). This document formally describes the structure that mappings located here need to follow. Here, we also try to give a clear explanation about why certain IR functions exist and how they integrate into the system.

## Eager and Lazy mappings

To understand the difference between eager and lazy mappings, it's benefitial for the reader to understand the optimization stages

### Optimization stages recap

In order to optimize the input program, the optimizer needs to gather information from both the input program and (often) from the underlying database management system. The reason is that the input program will rarely contain all the needed information, for example, the column names of the relations. The translation can be see as a two step process: procedural to IR, and IR to declarative. The two steps are detached, meaning the first step performs exclusively information gathering, resulting in a self-sufficient IR, and the second step performs exclusively IR translation and requires no access to the database and the input file. In other words, the two processes can (theoretically) be performed on different machines, at different times.

### Lazy mappings

Most of the mappings you will see in this folder are "lazy". This means that they do not need to be evaluated during the first stage of the optimization process (see Optimization stages recap). They __are__ the Intermediate Representation.

#### Examples:

- Column projection

- Row selection

- Join tables

### Eager mappings

Eager mappings are not part of the Intermediate Representation, but are an important part of the mapping process and all data libraries supporting RDBMS backends that want to make use of this optimizer need to have those. In other words, Eager mappings __help create__ the Intermediate Representation. 

#### Examples:

- Register database connection with the optimizer

- Fetch column data from the RDBMS

- Set database options
