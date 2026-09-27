"""
asyncio basics: run two coroutines concurrently as tasks.

Usage:
    python taskstogether.py
"""

import asyncio


async def fetch_data() -> dict:
    print("Start fetching")
    await asyncio.sleep(2)
    print("Done fetching")
    return {"data": 1235}


async def print_numbers() -> None:
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)


async def main() -> None:
    # TaskGroup (Python 3.11+) waits for every task and cancels the rest if one fails.
    async with asyncio.TaskGroup() as group:
        data_task = group.create_task(fetch_data())
        group.create_task(print_numbers())
    print(data_task.result())


if __name__ == "__main__":
    asyncio.run(main())
