import sys

import prefect
from prefect import Flow, task
from prefect.storage.module import Module


@task
def hello_task() -> None:
    logger = prefect.context.get("logger")
    logger.info(f"sys.path = {sys.path}")
    logger.info("Hello child!")


with Flow(
    "child",
    storage=Module(__name__),
) as flow:
    hello_task()
