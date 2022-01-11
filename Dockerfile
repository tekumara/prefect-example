FROM prefecthq/prefect:latest-python3.9

WORKDIR /workdir/

# python dependencies
COPY setup.py pyproject.toml ./
RUN pip install --no-cache-dir .

# code
COPY . .
