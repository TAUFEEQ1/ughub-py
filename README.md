
# ughub_py

[![codecov](https://codecov.io/gh/TAUFEEQ1/ughub-py/branch/main/graph/badge.svg?token=ughub-py_token_here)](https://codecov.io/gh/TAUFEEQ1/ughub-py)
[![CI](https://github.com/TAUFEEQ1/ughub-py/actions/workflows/main.yml/badge.svg)](https://github.com/TAUFEEQ1/ughub-py/actions/workflows/main.yml)

Awesome ughub_py created by TAUFEEQ1

## Install it from PyPI

```bash
pip install ughub_py
```

## Usage

```py
from ughub_py import Nira


base_url = "https://api.nira.com"
auth_token = "your_auth_token"

nira_api = NiraApi(base_url, auth_token)
person_data = nira_api.get_person(person_id)

```

```bash
$ python -m ughub_py
#or
$ ughub_py
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
