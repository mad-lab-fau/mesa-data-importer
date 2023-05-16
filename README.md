# MESA Data Importer

## Getting started
### Installation

Install the package using pip.

```
pip install git+https://mad-srv.informatik.uni-erlangen.de/MadLab/health-psychology/mesa-data-importer.git --upgrade
```

## For Developers

Install Python >=3.7 and [poetry](https://python-poetry.org).
Then run the commands below to get the latest source and install the dependencies:

```bash
git clone https://mad-srv.informatik.uni-erlangen.de/MadLab/health-psychology/mesa-data-importer.git
poetry install
```


To run any of the tools required for the development workflow, use the `doit` commands:

```bash
$ poetry run doit list
format               Reformat all files using black.
format_check         Check, but not change, formatting using black.
lint                 Lint all files with Prospector.
test                 Run Pytest with coverage.
```
