from django.shortcuts import render

import asyncio


async def first():
    print('George')
    # await second('Kibe')
    task = asyncio.create_task(second('Kibe'))
    await task
    print('Finished')


async def second(text):
    print(text)
    await asyncio.sleep(4)

asyncio.run(first)
