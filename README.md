<h1 align="center">Querpyable</h1>

<p align="center"><em>A Python implementation of LINQ</em></p>

<p align="center">
  <a href="https://www.python.org/">
    <img
      src="https://img.shields.io/pypi/pyversions/querpyable"
      alt="PyPI - Python Version"
    />
  </a>
  <a href="https://pypi.org/project/querpyable/">
    <img
      src="https://img.shields.io/pypi/v/querpyable"
      alt="PyPI"
    />
  </a>
  <a href="https://github.com/billsioros/querpyable/actions/workflows/ci.yml">
    <img
      src="https://github.com/billsioros/querpyable/actions/workflows/ci.yml/badge.svg"
      alt="CI"
    />
  </a>
  <a href="https://github.com/billsioros/querpyable/actions/workflows/cd.yml">
    <img
      src="https://github.com/billsioros/querpyable/actions/workflows/cd.yml/badge.svg"
      alt="CD"
    />
  </a>
  <a href="https://results.pre-commit.ci/latest/github/billsioros/querpyable/master">
    <img
      src="https://results.pre-commit.ci/badge/github/billsioros/querpyable/master.svg"
      alt="pre-commit.ci status"
    />
  </a>
  <a href="https://codecov.io/gh/billsioros/querpyable">
    <img
      src="https://codecov.io/gh/billsioros/querpyable/branch/master/graph/badge.svg?token=coLOL0j6Ap"
      alt="Test Coverage"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img
      src="https://img.shields.io/pypi/l/querpyable"
      alt="PyPI - License"
    />
  </a>
  <a href="https://gitpod.io/from-referrer/">
    <img
      src="https://img.shields.io/badge/Open%20on-Gitpod-blue?logo=gitpod&style=flat"
      alt="Open on Gitpod"
    />
  </a>
  <a href="https://github.com/billsioros/cookiecutter-pypackage">
    <img
      src="https://img.shields.io/badge/cookiecutter-template-D4AA00.svg?style=flat&logo=cookiecutter"
      alt="Cookiecutter Template">
  </a>
  <a href="https://app.renovatebot.com/dashboard#github/billsioros/querpyable">
    <img
      src="https://img.shields.io/badge/renovate-enabled-brightgreen.svg?style=flat&logo=renovatebot"
      alt="Renovate - Enabled">
  </a>
  <a href="https://www.buymeacoffee.com/billsioros">
    <img
      src="https://img.shields.io/badge/Buy%20me%20a-coffee-FFDD00.svg?style=flat&logo=buymeacoffee"
      alt="Buy me a coffee">
  </a>
  <a href="https://app.fossa.com/projects/custom%2B27372%2Fgithub.com%2Fbillsioros%2Fquerpyable/refs/branch/fix%2Fworking-version/f7d8508218ccd7057042a87c424029d8c98382d6">
    <img
      src="https://app.fossa.com/api/projects/custom%2B27372%2Fgithub.com%2Fbillsioros%2Fquerpyable.svg?type=shield"
      alt="FOSSA Status"
    />
  </a>
</p>

## :bulb: Example

> Calculating the first 10000 primes

```python
Queryable \
  .range(2, 1_000_000) \
  .where(lambda n: all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))) \
  .take(10000)
```

## :cd: Installation

```bash
pip install querpyable
```

In order to locally set up the project please follow the instructions below:

```shell
# Set up the GitHub repository
git init
git config --local user.name Vasilis Sioros
git config --local user.email billsioros97@gmail.com
git add .
git commit -m "feat: initial commit"
git remote add origin https://github.com/billsioros/querpyable

# Create a virtual environment using poetry and install the required dependencies
poetry shell
poetry install

# Install pre-commit hooks
pre-commit install --install-hooks
```

## :book: Documentation

The project's documentation can be found [here](https://billsioros.github.io/querpyable/).

## :heart: Support the project

Feel free to [**Buy me a coffee! ☕**](https://www.buymeacoffee.com/billsioros).

## :sparkles: Contributing

If you would like to contribute to the project, please go through the [Contributing Guidelines](https://billsioros.github.io/querpyable/latest/CONTRIBUTING/) first.

## :label: Credits

This project was generated with [`billsioros/cookiecutter-pypackage`](https://github.com/billsioros/cookiecutter-pypackage) cookiecutter template.
