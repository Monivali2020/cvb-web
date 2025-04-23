import asyncio
import datetime

scheduled_tasks = []

def schedule_task(delay_seconds, callback, *args, **kwargs):
    task = asyncio.create_task(run_after_delay(delay_seconds, callback, *args, **kwargs))
    scheduled_tasks.append(task)

async def run_after_delay(delay_seconds, callback, *args, **kwargs):
    await asyncio.sleep(delay_seconds)
    await callback(*args, **kwargs)

def cancel_all_tasks():
    for task in scheduled_tasks:
        if not task.done():
            task.cancel()