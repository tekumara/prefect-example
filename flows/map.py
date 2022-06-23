from typing import List

import prefect
from prefect import Flow, task, unmapped


@task
def setup() -> str:
    return "done"


@task
def fetch_batches() -> List[str]:
    return ["batch"] * 10


@task
def count_rows(batch: str) -> int:
    return 1


@task
def summary(count: List[int]) -> None:
    logger = prefect.context.get("logger")
    total = sum(count)
    logger.info(f"Num batches: {len(count)} Num rows: {total}")
    return None


with Flow(
    "map-flow",
) as flow:
    batches = fetch_batches()
    counts = count_rows.map(batches, upstream_tasks=[unmapped(setup())])
    summary(counts)

flow.run()
