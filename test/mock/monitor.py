import random
# from .. import log

# logger = log.getLogger(__name__)
# logger.info("Mocking execution")


def timeit(fn, *args, **kwargs):
    result = fn(*args, **kwargs)
    return result, random.randint(100, 800)


class Monitor:
    def __init__(self, *args, **kwargs):
        self.diffs = [random.randint(1000, 8000)] * random.randint(20, 40)
        self.oom = True if random.randint(0, 1) else False
        self.time = random.randint(100, 800)
