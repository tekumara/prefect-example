from flows.dask_flow import transform


def test_transform():
    assert transform.run(2) == 4  # type: ignore
