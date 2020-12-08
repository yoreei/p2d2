# Private Repository of Yordan Grigorov's bachelor thesis

## Bachelor thesis link:


## TODO
list of mappings
IR
pandas to IR
SQL to IR

## Dir structure

**grizzly**
   - Scripts that prepare *workflows* for execution with grizzly
   - Experiments with grizzly

**modin**
   - Scripts that prepare *workflows* for execution with modin
   - Experiments with modin

**p2d2**
   - The product of the thesis
   - "**P**ython **P**ush**D**own to **D**atabase _Management System_"

**papers**
   - PDFs of papers that are/were referenced by the thesis
   - PDFs of papers that I find interesting and could be relevant for the thesis

**wflows**
   - Data science workflows adapted from Kaggle
   **wflows/qgenenv** - contains the *qgen* binary from TPC-H and its output (result.sql, result2.sql, result3.sql) 

**data**
   - Data for the wflows and the scripts to import them. See comments in wflows to see what data is required. Or just import all.

**tpch-kit**
   - submodule containing gregrahn's fork of the TPC-H implementation. I had some difficulties compiling the original TPC-H and also this fork promises better PostgreSQL compatibility.

**latex**
   - The bachelor thesis

**retired**
   - The "trash bin". Contains code I might not want to delete just yet.

