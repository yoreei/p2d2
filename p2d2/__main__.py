#!/usr/bin/env python3
from p2d2.benchmarker import finished_hook
import p2d2.benchmarker.main as main 
# import p2d2.benchmarker.bench_main as main 
import sys
import getpass

if getpass.getuser() != 'root':
    print("run as root")
    exit()

# check if ray is set up
# import ray
# ray.init(address='auto', _redis_password='root')
# ray.shutdown()


if sys.argv[1] == 'kaggle':
    main = main.kaggle_main
elif sys.argv[1] == 'micro':
    main = main.micro_main
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
