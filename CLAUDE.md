# Project Configuration for Claude Code

## Virtual Environment
This project uses **uv** for Python package management.

### Running Python Commands
- **Always use**: `uv run python <command>`
- **Example**: `uv run python main.py`

### Virtual Environment Activation
uv automatically manages the virtual environment. No manual activation needed.

For manual operations:
```bash
# uv automatically creates and manages .venv/
# If needed, activate manually:
source .venv/bin/activate
```

### Package Management
- **Install dependencies**: `uv pip install <package>`
- **Add to project**: `uv add <package>`
- **Sync dependencies**: `uv sync`

## Python Version
- Required: Python >=3.12 (specified in pyproject.toml)
- Current: 3.13 (from .python-version)

## Project Structure
- `main.py`: Main application entry point
- `pyproject.toml`: Project configuration and dependencies
- `.python-version`: Python version specification for uv
