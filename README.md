# Python Specific Provisioner

This REST application mocks a specific provisioner for data product components.

This project uses OpenAPI as standard API specification and the [fastapi-code-generator](https://pypi.org/project/fastapi-code-generator/)

#### Setup Python environment
To set up a Python environment we use [Poetry](https://python-poetry.org/docs/):

```
curl -sSL https://install.python-poetry.org | python3 -
```
Once Poetry is installed and in your `$PATH`, you can execute the following:
```
poetry --version
```
If you see something like `Poetry (version x.x.x)`, your install is ready to use!

Install the dependencies defined in `specific-provisioner/pyproject.toml`:
```
cd specific-provisioner
poetry install
```