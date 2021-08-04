import datetime

from aiohttp import web
from scheduler import (
    health_http_handler,
    register_periodic_tasks,
    cancel_periodic_tasks,
    create_task,
    test
)

# Test task to check if periodic works
create_task('test1', test, datetime.timedelta(seconds=1), number=1)
create_task('test2', test, datetime.timedelta(seconds=2), number=2)
create_task('test3', test, datetime.timedelta(seconds=3), number=3)
create_task('test4', test, datetime.timedelta(seconds=4), number=4)
create_task('since', test, datetime.timedelta(seconds=1), since=datetime.datetime.now()+datetime.timedelta(seconds=4), number=5)


app = web.Application()
app.add_routes([web.get('/health', health_http_handler)])
app.on_startup.append(register_periodic_tasks)
app.on_cleanup.append(cancel_periodic_tasks)


def start():
    web.run_app(app)


if __name__ == '__main__':
    start()
