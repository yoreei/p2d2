#!/usr/bin/env python3
from p2d2.benchmarker import finished_hook
import p2d2.benchmarker.main as main 
# import p2d2.benchmarker.bench_main as main 
import sys
if sys.argv[1] == 'kaggle':
    main = main.kaggle_main
elif sys.argv[1] == 'micro':
    main = main.kaggle_micro
else:
    print('kaggle or micro')
    exit()

if __name__ == "__main__":
    try:                                                 
        main()
    except Exception as e:                               
        raise e                                          
    finally:                                             
        finished_hook.fire()                             
