#!/usr/bin/env python3
"""Measure the runtime"""
from time import perf_counter
import asyncio
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """Create a measure_time function"""
    begin = perf_counter()
    asyncio.run(wait_n(n, max_delay))
    elapsed = perf_counter() - begin
    return elapsed / n
