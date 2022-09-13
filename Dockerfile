FROM python:3.9-slim

WORKDIR /workdir/

# tell prefect where to find our package code
ENV PYTHONPATH=/workdir/

# needed to build psutil on arm64
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# python dependencies
COPY setup.py pyproject.toml ./
RUN pip install --no-cache-dir -e .

# code
COPY . .
