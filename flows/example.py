import sys

import prefect
from prefect import Flow, task
from prefect.run_configs import KubernetesRun
from prefect.storage.module import Module

import flows.another_module


@task
def hello_task() -> None:
    logger = prefect.context.get("logger")
    logger.info(f"sys.path = {sys.path}")
    logger.info(flows.another_module.msg)
    logger.info("Goodbye world!")


with Flow(
    "hello-flow",
    storage=Module(__name__),
    run_config=KubernetesRun(
        image="prefect-registry:5000/prefect-example:v1",
        labels=["kube"],
        cpu_limit=1,
        cpu_request=1,
        memory_limit="1Gi",
    ),
) as flow:
    hello_task()
