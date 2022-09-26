from typing import List

import prefect
from prefect import Flow, flatten, task, unmapped


@task
def setup() -> str:
    logger = prefect.context.get("logger")
    logger.info("setup")
    return "done"


@task
def fetch_batches() -> List[str]:
    return [f"batch {i}" for i in range(10)]


@task
def repartition_batches(batch: str) -> List[List[str]]:
    logger = prefect.context.get("logger")
    batch_size = 4
    materialised = [f"{batch}-{i}" for i in range(8)]
    repartitioned = [materialised[i : i + batch_size] for i in range(0, len(materialised), batch_size)]
    logger.info(f"Breaking result batch of size {len(materialised)} into {len(repartitioned)} batches")
    return repartitioned


@task
def count_rows(batch: List[str]) -> int:
    logger = prefect.context.get("logger")
    logger.info(batch)
    return len(batch)


@task
def summary(count: List[int]) -> None:
    logger = prefect.context.get("logger")
    logger.info(f"{count} Num batches: {len(count)} Num rows: {sum(count)}")
    return None


with Flow(
    "flatten-flow",
) as flow:
    logger = prefect.context.get("logger")
    batches = fetch_batches()
    balanced_batches = repartition_batches.map(batches)
    # unmapped is needed to process all inputs see https://github.com/PrefectHQ/prefect/issues/5927
    # flatten unwraps the batch
    counts = count_rows.map(flatten(balanced_batches), upstream_tasks=[unmapped(setup())])
    # without flatten: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2] Num batches: 10 Num rows: 20
    # with flatten:    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4] Num batches: 20 Num rows: 80
    summary(counts)

flow.visualize()
flow.run()
