import sys

import prefect
from prefect import Flow, task
from prefect.run_configs import KubernetesRun
from prefect.storage.module import Module

import flows.another_module


@task
def hello_task(name: str) -> None:
    logger = prefect.context.get("logger")
    logger.info(f"sys.path = {sys.path}")
    logger.info(flows.another_module.msg)
    logger.info(f"Goodbye {name}!")


with Flow(
    "hello-flow",
    storage=Module(__name__),
    run_config=KubernetesRun(
        image="prefect-registry:5555/prefect-example:v1",
        labels=["kube"],
        cpu_limit=1,
        cpu_request=1,
        memory_limit="1Gi",
        # needed to get pull latest version of a mutated image tag
        image_pull_policy="Always",
    ),
) as flow:
    hello_task("world")


if __name__ == "__main__":
    flow.run()
