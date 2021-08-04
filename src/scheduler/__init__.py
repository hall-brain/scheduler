import asyncio
import datetime
import json
from typing import Optional, NoReturn, Callable
import logging

from aiohttp import web


logging.basicConfig(level=logging.DEBUG)

tasks = {}


async def wait_until_since(since: Optional[datetime.datetime]) -> NoReturn:
    """
    Sleep for since - now() seconds.
    :param since: Datetime when the function should end.
    :return: None
    """
    if since:
        await asyncio.sleep((since - datetime.datetime.now()).total_seconds())


async def periodic_wrapper(
    func: Callable,
    interval: datetime.timedelta,
    since: Optional[datetime.datetime] = None,
    func_await: bool = True,
    **func_kwargs,
) -> NoReturn:
    """
    This function is used to create periodic tasks. It wraps core function (func)
    and runs it periodically. Supports full time range.
    :param func: callable which asyncio.Task should execute
    :param interval: how often func should be called
    :param since: when the function should be called the first time
    :param func_await: is function async or sync
    :param func_kwargs: named arguments for func
    :return: None
    """
    try:
        await wait_until_since(since)
        while True:
            await asyncio.sleep(interval.total_seconds())
            if func_await:
                await func(**func_kwargs)
            else:
                func(**func_kwargs)
    except asyncio.CancelledError:
        pass


def create_task(
    name: str,
    func: Callable,
    interval: datetime.timedelta,
    since: Optional[datetime.datetime] = None,
    func_await: bool = True,
    **func_kwargs,
) -> asyncio.Task:
    """
    Create asyncio.Task using periodic wrapper to make task periodic.
    :param func: callable which should be executed periodically
    :param interval: how often func should be called
    :param since: when the function should be called the first time
    :param func_await: is function async or sync
    :param func_kwargs: named arguments for func
    :return: asyncio.Task
    """
    task = asyncio.Task(
        periodic_wrapper(
            func=func,
            interval=interval,
            since=since,
            func_await=func_await,
            **func_kwargs,
        )
    )
    tasks[name] = task
    return task


async def register_periodic_tasks(app):
    for name, task in tasks.items():
        app[name] = task


async def cancel_periodic_tasks(app):
    for name, task in tasks.items():
        task.cancel()


async def health_http_handler(request):
    logging.info('Health API requested')
    return web.Response(
        text=json.dumps({'status': 'ok', 'tasks': len(asyncio.all_tasks())})
    )


async def test(number):
    logging.info(f'Starting number: {number}')
    await asyncio.sleep(1)
    logging.info(f'Finishing number: {number}')
