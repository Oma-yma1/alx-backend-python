#!/usr/bin/env python3

""" The basics of async"""
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """asynchronous coroutine that takes in an integer arg"""
    rand_value = random.uniform(0, max_delay)
    await asyncio.sleep(rand_value)
    return rand_value
