import asyncio
import concurrent.futures
import logging
import sys
from functools import partial

from .op_1 import init_operation, operation

logging.basicConfig(
    level=logging.INFO,
    format="Worker[%(process)5s] %(name)40s: %(message)s",
    stream=sys.stderr,
)


async def run_operations_in_executor(number, executor):
    loop = asyncio.get_event_loop()

    for i in range(number + 1):
        operation_ref = partial(operation, {"ContextKey": f"Value for data {i}"})
        await loop.run_in_executor(executor, operation_ref, i)
    

if __name__ == "__main__":
    # Create a limited thread pool.
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=3, initializer=init_operation)
    asyncio.run(run_operations_in_executor(15, executor))
    print("Done")
