FROM python:3.9-slim

WORKDIR /workdir/

# python dependencies
COPY setup.py pyproject.toml ./
RUN pip install --no-cache-dir -e .

# code
COPY . .
