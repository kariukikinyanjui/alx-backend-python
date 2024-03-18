#!/usr/bin/env python3
"""Create and manage coroutines"""
import asyncio
import time
from typing import List
wait_n = __import__('1-concurrent_coroutines').wait_n


async def measure_time(n: int, max_delay: int) -> List[float]:
    """
    Measure the total execution time of wait_n(n, max_delay) and
    returns the average time per call (total_time / n).

    Args:
        n: The numer of times to spawn wait_random.
        max_delay: The maximum delay for each wait random call.

    Returns:
       The average execution time per wait_n call (float)
    """
    start_time = time.time()
    await wait_n(n, max_delay)
    end_time = time.time()

    total_time = end_time - start_time
    return total_time / n