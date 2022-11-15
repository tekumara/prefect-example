import logging

import prefect
from prefect import Flow, task
from prefect.run_configs import KubernetesRun
from prefect.storage.module import Module

python_logger = logging.getLogger(__name__)
print(__name__)


@task
def loggers_task() -> None:
    prefect_logger = prefect.context.get("logger")
    prefect_logger.info("info from the prefect logger")
    prefect_logger.warning("warning from the prefect logger")
    python_logger.info("info from python logger")
    python_logger.warning("warning from python logger")


@task
def second_task() -> None:
    python_logger.info("python logging from a second task to show its associated with this task and not loggers_task")


with Flow(
    "loggers-flow",
    storage=Module(__name__),
    run_config=KubernetesRun(
        image="prefect-registry:5555/prefect-example:v1",
        labels=["kube"],
        cpu_limit=1,
        cpu_request=1,
        memory_limit="1Gi",
        # needed to get pull latest version of a mutated image tag
        image_pull_policy="Always",
        # see https://docs-v1.prefect.io/core/concepts/logging.html#extra-loggers
        env={"PREFECT__LOGGING__EXTRA_LOGGERS": "['flows.loggers']"},
    ),
) as flow:
    loggers_task()
    second_task()

if __name__ == "__main__":
    flow.run()
