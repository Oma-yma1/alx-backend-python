#!/usr/bin/env python3
""" task1"""
import asyncio
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """write a coroutine called async_comprehension that takes no argument"""
    return [i async for i in async_generator()]
