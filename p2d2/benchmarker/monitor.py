import multiprocessing as mp
import pandas

mp.set_start_method("spawn")
import psutil
import time

def available():
    return psutil.virtual_memory().available

def monitor(code_str, globals_passed, locals_passed) -> dict:
    bytes_memory = []
    cpu_percent = []
    net_io_start = psutil.net_io_counters(pernic=True, nowrap=True)['lo']
    mon_df = pandas.DataFrame()

    locals_passed['SHARED_DB_TIME'] = mp.Value('f',0)
    args = (code_str, globals_passed, locals_passed)
    start_mem = available()
    p = mp.Process(target=exec, args=args)
    start_clock = time.perf_counter()
    p.start()
    while p.exitcode == None:
        bytes_memory.append(start_mem - available())
        cpu_percent.append(psutil.cpu_percent(interval=None, percpu=True))
        p.join(0.08)
    
    end_clock = time.perf_counter()
    net_io_end= psutil.net_io_counters(pernic=True, nowrap=True)['lo']
    bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
    bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv
    mon_df['bytes_memory'] = bytes_memory
    mon_df['cpu_percent'] = cpu_percent
    mon_df['bytes_sent'] = bytes_sent
    mon_df['bytes_recv'] = bytes_recv
    

    mon_df['wall_time'] = end_clock - start_clock
    mon_df['exitcode'] = p.exitcode # -9 for oom
    mon_df['db_time'] = locals_passed['SHARED_DB_TIME'].value
    # insert process_snapshot
    mon_df.reset_index(drop=False, inplace=True)
    mon_df.rename({'index':'process_snapshot'}, inplace=True)
    return mon_df
