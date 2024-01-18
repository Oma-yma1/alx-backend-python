#!/usr/bin/env python3
""" task2"""
import asyncio
from time import perf_counter
from typing import List
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measure_runtime should measure the total runtime and return it"""
    a = perf_counter()
    task = [asyncio.create_task(async_comprehension()) for i in range(4)]
    await asyncio.gather(*task)
    runtime = perf_counter() - a
    return runtime
