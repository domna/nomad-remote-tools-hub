[![pipeline status](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/badges/main/pipeline.svg)](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/commits/main)
[![coverage report](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/badges/main/coverage.svg)](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/commits/main)

# NOMAD remote tools hub (north)

Lets you run containarized tools remotly.

## Getting started

Clone the project

```sh
git clone git@gitlab.mpcdf.mpg.de:nomad-lab/nomad-remote-tools-hub.git
cd nomad-remote-tools-hub
```

Optionaly, checkout the desired branch (e.g. develop) and create a feature branch
```
git checkout develop
git checkout -b my-feature
```

Create a virtual environment based on Python 3 (>3.7).
```sh
pip install virtualenv
virtualenv -p `which python3` .pyenv
source .pyenv/bin/activate
```

Install the nomad-remote-tools-hub package.
```sh
pip install -e .
```

Run the app with uvivcorn:
```sh
uvicorn north.app.main:app
```

Run the tests with pytest:
```sh
pytest -svx test
```

We recomment using vs-code. Here are vs-code settings that match the CI/CD linting:
```json
{
    "python.pythonPath": ".pyenv/bin/python",
    "editor.rulers": [90],
    "editor.renderWhitespace": "all",
    "editor.tabSize": 4,
    "files.trimTrailingWhitespace": true,
    "python.linting.pycodestylePath": "pycodestyle",
    "python.linting.pycodestyleEnabled": true,
    "python.linting.pycodestyleArgs": ["--ignore=E501,E701,E731"],
    "python.linting.mypyEnabled": true,
    "python.linting.pylintEnabled": true,
}
```

## Project structure

- `north` - The Python code
- `north/app` - The [FastAPI](https://fastapi.tiangolo.com/) application that runs the north app
- `north/config` - All applications settings
- `tests` - The [pytest](https://docs.pytest.org/) tests
- `setup.py` - Install the package with pip
- `docker` - All the docker files, scripts for creating/managing images, documentation
