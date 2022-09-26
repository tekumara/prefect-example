from typing import List

import prefect
from prefect import Flow, task, unmapped


@task
def setup() -> str:
    logger = prefect.context.get("logger")
    logger.info("setup")
    return "done"


@task
def fetch_batches() -> List[str]:
    return [f"batch {i}" for i in range(10)]


@task
def count_rows(batch: str) -> int:
    logger = prefect.context.get("logger")
    logger.info(f"{batch}")
    return 1


@task
def summary(count: List[int]) -> None:
    logger = prefect.context.get("logger")
    logger.info(f"{count} Num batches: {len(count)} Num rows: {sum(count)}")
    return None


with Flow(
    "map-flow",
) as flow:
    batches = fetch_batches()
    # unmapped is needed to process all inputs see https://github.com/PrefectHQ/prefect/issues/5927
    counts = count_rows.map(batches, upstream_tasks=[unmapped(setup())])
    summary(counts)

flow.run()
