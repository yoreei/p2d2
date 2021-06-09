import multiprocessing as mp

mp.set_start_method("spawn")
import psutil
import time


def timeit(fn, *args, **kwargs):
    start_clock = time.perf_counter()
    # fn is usually Monitor.spawn at this point
    result = fn(*args, **kwargs)
    end_clock = time.perf_counter()
    timeit_time = end_clock - start_clock
    return (result, timeit_time)


class Monitor:
    """Executes a function in a different process and records memory and time usage"""
    def spawn(self, fn, *args, **kwargs):
        self.start_mem = self.available()
        # fn is usually exec at this point
        # args contains the code string
        p = mp.Process(target=fn, args=args, kwargs=kwargs)
        p.start()
        while p.exitcode == None:
            self.diffs += [self.start_mem - self.available()]
            # print(self.diffs[-1])
            p.join(0.01)
        if p.exitcode == -9:
            self.oom = True
        self.exitcode = p.exitcode

    def available(self):
        return psutil.virtual_memory().available

    def __init__(self, fn, *args, **kwargs):
        self.oom = False
        self.diffs = []
        _, self.time = timeit(self.spawn, fn, *args, **kwargs)
