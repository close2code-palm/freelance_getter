"""some core functions that are class-independent"""

import asyncio

from aiohttp import ClientSession


async def get_sp(url:str='https://freelance.habr.com/tasks'):
    """asyncronious parsing core fun"""
    async with ClientSession() as sessn:
        async with sessn.get(url, raise_for_status=False) as resp_pg:
            # pg_dt = await resp_pg.read()
            # print(await resp_pg)
            # pg_dt = pg_dt.decode('utf-8')
            return resp_pg
# def rnr()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(get_sp())

