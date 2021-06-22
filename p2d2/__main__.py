#!/usr/bin/env python3
from benchmarker import finished_hook
import p2d2.benchmarker.kaggle_main as main 
# import p2d2.benchmarker.bench_main as main 

if __name__ == "__main__":
    try:                                                 
        main()
    except Exception as e:                               
        raise e                                          
    finally:                                             
        finished_hook.fire()                             
