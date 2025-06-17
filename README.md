# FARI Digital Twin Backend V2

This project is the backend for the FARI Digital Twin.

## Installation

This project uses `uv` for dependency management.

1.  Create and activate a virtual environment:
    ```bash
    uv venv
    source .venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    uv pip sync pyproject.toml
    ```

## Running the application

Run the main script:
```bash
uv run python main.py
``` 