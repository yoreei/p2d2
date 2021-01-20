# Statistics for the Optimizer

To obtain as much value from the benchmarks as possible, a flexible benchmarking framework will be built. Ideally, we should have the factors:

1. scale10 / scale20 / scale30 /... scale200 (tpch scale factor used in the benchmark)

2. warm_up / no_warm_up

3. index / no_index

4. opt_include / opt_exclude / no_opt  (if optimization time should be included/excluded or if not optimization should be performed)

5. net_local / net_lan / net_wan ("stealing" this from the Don't hold my data hostage paper)

And the following response variables:

wall_time, db_time, mem_usage_db, mem_usage_py, network_utilization, cpu utilization

## The measurements in-depth:

- What does mem_usage mean? Average / *Maximum*?
- What tool(s) do we use to perform the measurements? is *top* enough?
- At what interval should they be measured to balance correctness/performance impact?
- How do we measure mem_usage_db? Do we take the (peak/average) mem usage und substract the idle mem usage?

### wall_time

We already measure this with Python's timeit module

### db_time

requires
```
shared_preload_libraries = 'pg_stat_statements' # (change requires restart)
```

inside postgresql.conf and
```
CREATE EXTENSION pg_stat_statements
```

inside the database

1. Clear all stats before running the worklow:

```
select pg_stat_statements_reset();
```

2. Run the workflow

3. Query the total time:

```
SELECT sum(total_time) from pg_stat_statements
WHERE queryid != 4127066443358369148;
```

#### db_time explanation:

```
SELECT queryid, query, total_time, calls from pg_stat_statements;
```

The output:

queryid|query|total_time|calls
---------------------|-----------------------------------|------------|-------
 4127066443358369148 | select pg_stat_statements_reset() |   0.174501 |     1
 8824814412070308173 | select * from customer            | 145.979456 |     1

The output will contain as many rows as the number of queries that the optimizer decided to construct from the workflow + an additional row representing the pg_stat_statements_reset() function. To exclude the reset function we can use its id. This id can be assumed to be unique for a single installation of postgresql, but this is not guaranteed across different builds of postgresql. In any case, it does not add any significant total_time.

*calls* is the number of time this query has been executed. In our case this should always be 1, if not, our optimizer is to blame.

*total_time* is acumulative, which means that we don't have to calculate total_time\*calls to account for duplicate queries - that's already done for us.


### mem_usage_db and mem_usage_py,

Recap: The optimized AND unoptimized versions of the workflow run *inside* the process of the benchmarker. The benchmarker process "hangs" until the workflow is finished, so to look at the RAM usage of the DB we need to create another thread which will monitor postgresql's memory usage during execution. What tools can we use to monitor the memory?

from *man top*:

```
                               Private | Shared
                           1           |          2
      Anonymous  . stack               |
                 . malloc()            |
                 . brk()/sbrk()        | . POSIX shm*
                 . mmap(PRIVATE, ANON) | . mmap(SHARED, ANON)
                -----------------------+----------------------
                 . mmap(PRIVATE, fd)   | . mmap(SHARED, fd)
    File-backed  . pgms/shared libs    |
                           3           |          4

 The  following  may  help  in interpreting process level memory values displayed as scalable columns and dis‐
 cussed under topic `3a. DESCRIPTIONS of Fields'.

    %MEM - simply RES divided by total physical memory
    CODE - the `pgms' portion of quadrant 3
    DATA - the entire quadrant 1 portion of VIRT plus all
           explicit mmap file-backed pages of quadrant 3
    RES  - anything occupying physical memory which, beginning with
           Linux-4.5, is the sum of the following three fields:
           RSan - quadrant 1 pages, which include any
                  former quadrant 3 pages if modified
           RSfd - quadrant 3 and quadrant 4 pages
           RSsh - quadrant 2 pages
    RSlk - subset of RES which cannot be swapped out (any quadrant)
    SHR  - subset of RES (excludes 1, includes all 2 & 4, some 3)
    SWAP - potentially any quadrant except 4
    USED - simply the sum of RES and SWAP
    VIRT - everything in-use and/or reserved (all quadrants)
```

Now, which memory measurement should we use? _RES_ seems like a good choice?

### network_utilization

We need to be able to measure the size of the data that is transfered from the DB to the Python runtime.

EXPLAIN [QUERY] can give us this information:

```
Seq Scan on lineitem  (cost=0.00..172517.01 rows=6001401 width=4)
```

"width" tells us the size of a single row in bytes. So, to calculate the network utilization, we use 'rows\*width'.

This calculation does not take into account any compression techniques but it should suffice for our purposes.

#### Network utilization: Implementation detail:

After running the data science workflow, the benchmarker will extract the queries produced by the optimizer and run an EXPLAIN query on them. To easily extract the queries we can use pg_stat_statements

### CPU

Considering that we are already measuring a lot, measuring CPU utilization might be superfluous. The problem is, _we "promised" this in the proposal_.

both time and top give info about CPU utilization but check this out:

http://www.brendangregg.com/blog/2017-05-09/cpu-utilization-is-wrong.html

(that doesn't mean we shouldn't use top, but it's useful to know WHAT we are measuring)


## Factors in-depth

### Bandwidth limit:

"Don't hold my data hostage" used netem for this. We can assume this is a good way to do this.

- Local: The server and client reside on the same machine, there are no network restrictions.

- LAN: The  server  and  client  are  connected using a gigabit ethernet connection with 1000Mb/s throughput and 0.3ms latency.

- WAN: The server and client are connected through an internet connection, the network is restricted by 100 Mbit/s throughput, 25ms latency and 1.0% uniform random packet loss.


https://serverfault.com/questions/507658/limit-incoming-and-outgoing-bandwidth-and-latency-in-linux

## Value/Cost ratio

In practice, some of these variables might not be worth considering the cost adds up _exponentially_.

the _bandwidth_ variable probably needs shrinking/trimming, I am open to suggestions.

## Benchmark Dataframe anatomy

This document will present two options for recording measurement data and will weigh the pros and cons of each. Excuse my bad statistics terminology:

### The "Variable" method:

Example Dataframe: 

i   scale   warm_up index  opt_include net_limit   |   wall_time   cpu_utilization mem_usage_db    mem_usage_py    MB_served
1   10      False   False       0           50              10000       
2
3
4
5
6
7
8
9


Interesting article about benchmarking with top and awk: https://yunmingzhang.wordpress.com/2014/04/01/using-top-ps-and-awk-for-benchmarking-cpu-and-memory-utilization-in-a-cluster-environment/

pre_once_l=['warm_up', 'no_warm_up']
pre_every_l=['index', 'no_index']
stopwatch_l=['stopwatch_opt', 'stopwatch_noopt']


# Retired text
GNU time:
```
command time -v python3 wflows/joinprojsel.py

Command being timed: "python3 wflows/joinprojsel.py"
User time (seconds): 6.84
System time (seconds): 1.49
Percent of CPU this job got: 21%
Elapsed (wall clock) time (h:mm:ss or m:ss): 0:39.45
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 1305720 <---- about 1 GB seems alright
Average resident set size (kbytes): 0 <---- why!?
Major (requiring I/O) page faults: 6608
Minor (reclaiming a frame) page faults: 368115
Voluntary context switches: 36730
Involuntary context switches: 116
Swaps: 0
File system inputs: 244856
File system outputs: 0
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0 
```