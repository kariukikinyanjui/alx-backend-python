#!/usr/bin/env python
"""
Modules used to create and manage coroutines and offers functions
for generating random numbers
"""
import asyncio
import random


async def async_generator():
    """
    An asynchronous generator that yields random numbers
    between 0 and 10
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.randint(0, 10)
