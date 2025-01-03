from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timeit() -> float:
    start = perf_counter()
    end = start
    yield lambda: end - start
    end = perf_counter()
