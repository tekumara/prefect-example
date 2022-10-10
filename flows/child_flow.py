import sys
from time import sleep

import prefect
from prefect import Flow, task
from prefect.run_configs import KubernetesRun
from prefect.storage.module import Module


@task
def sleepy() -> None:
    logger = prefect.context.get("logger")
    logger.info(f"sys.path = {sys.path}")
    logger.info("Hello child!")
    logger.info("Sleeping.....")
    sleep(5 * 60)
    logger.info("Awake!")


with Flow(
    "child",
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
    sleepy()
