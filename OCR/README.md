## OCR

### Installation

```shell
pipx install poetry
```

Activate the virtual environment and install dependencies, all subsequent commands assume you are in the virtual env
```shell
poetry shell
poetry install
```

Run unit tests
```shell
poetry run pytest
```

Run benchmark tests
```shell
poetry run pytest bench_test.py -v
```

poetry run pytest bench_test.py -v  

Run main, hoping to convert this to a cli at some point
```shell
poetry run main
```


Adding new dependencies
```shell
poetry add package-name
```

To manually update the poetry lock file
```shell
poetry lock
```

To view installed packages in the virtual env
```shell
poetry show
```

To lint your files using ruff
```shell
ruff check --fix
```

To format your files using ruff 
```shell
ruff format
```