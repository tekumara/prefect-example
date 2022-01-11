import sys

import prefect
from prefect import Flow, task

import flows.another_module


@task
def hello_task():
    logger = prefect.context.get("logger")
    logger.info(f"sys.path = {sys.path}")
    logger.info(flows.another_module.msg)


with Flow("hello-flow") as flow:
    hello_task()

# for local testing
if __name__ == "__main__":
    flow.run()
