#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here
   and here
   and ...
"""

import asyncio
import random

# each color represent a employee
colors = (
    "\033[0m",    # End of color
    "\033[36m",   # Cyan
    "\033[91m",   # Red
    "\033[35m",   # Magenta
    "\033[33m",   # Yellow
    "\033[32m",   # Green
    "\033[34m",   # Blue
)

# each employee has a name
names = (
    "Leandro",
    "Sophia",
    "Alexandra",
    "Jack",
    "Pedro",
    "Maria"
)

# all the employees share any of these tasks
jobs = (
    "PRINT FILES",
    "CREATE DOCUMENTS",
    "MAKE FILE COPIES",
    "SEARCH DOCUMENTS ONLINE",
    "SEND DOCUMENTS ON E-MAIL",
    "DELETE FILES",
    "UPDATE FILES",
    "INSPECT FILES FROM EMAIL",
    "CHECK FOR VIRUS ON COMPUTER",
    "UPDATE EXCEL",
    "MAKE REPORTS"
)

# the company has a employer and a name
employer = "Marco"
company = "Deployment"


# this function makes random tasks with random time to complete
async def makeTask() -> tuple:
    return (jobs[random.randint(0, 6)], random.uniform(1.5, 4))


# here, each employees is set to a specif task
async def employee(name: str, color: str, queue: asyncio.Queue) -> None:

    while True:
        # Get a item from ther queue for the worker to work on it.
        task, time = await queue.get()
        print(color + f"{name} is making the task {task}, Queue: {queue.qsize()}" + colors[0])
        await asyncio.sleep(time)

        print(color + f"---{name} completed the task {task} in {time:.2f} seconds." + colors[0])

        queue.task_done()
    
    return

# here, the employer get update that the queue is getting low and fill more tasks until the end of the day
async def employer(queue: asyncio.Queue) -> None:
    n = random.uniform(1, 3)
    while True:
        task = await makeTask()
        queue.put_nowait(task)
        print(f"New task available: {task[0]}, Queue: {queue.qsize()}")
        await asyncio.sleep(n)
    return

async def company(N: int) -> None:

    queue = asyncio.Queue() # queue structure for the jobs to be done

    # the day starst with pre planed tasks
    for _ in range(N):
        queue.put_nowait(await makeTask())

    # hiring employees for the company
    employees = [asyncio.create_task(
            employee(names[i], colors[1+i], queue)) for i in range(len(names))
        ]
    
    # the employer arrives at the company and will fire many tasks
    asyncio.gather(employer(queue=queue), return_exceptions=True)

    # The crucial command!!! 
    # Join will block the application here.
    # It will only let the code to continue once the queue is empty!!!
    # Each call of task_done() will send a protocal to indicate that the task has been done.
    # Can you imagine why eventually all the tasks will be completed?
    await queue.join()


    # Cancel our employees which can now go home
    for i in employees:
        i.cancel()

    

if __name__ == "__main__":
    random.seed(20)
    asyncio.run(company(10))