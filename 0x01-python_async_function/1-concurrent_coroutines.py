#!/usr/bin/env python3
"""
Create and manage coroutines
import wait_random from 0-basic_async_syntax
"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawns wait_random n times with the specified max_delay

    Args:
        n: The number of times to spawn wait_random
        max_delay: The maximum delay for each wait_random coroutine

    Returns:
        A list of the delays in ascending order
    """

    delays: list[float] = []
    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]

    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.insert(0, delay)

    return delays
