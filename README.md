# Foundry Agent Structured Input/Output

A small Python example showing how to structure a Microsoft Foundry agent project with separate modules.

## Project layout

- `foundryagent_structureinput_output.py` - root script entrypoint
- `foundryagent_structureinput_output/` - package modules
  - `config.py` - environment configuration
  - `schemas.py` - Pydantic data models and JSON schema helpers
  - `agent.py` - Foundry agent creation and call logic
  - `main.py` - program flow and example request

## Setup

1. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install requirements:
   ```powershell
   pip install -r requirements.txt
   ```

3. Add `.env` values:
   ```text
   PROJECT_ENDPOINT=<your-project-endpoint>
   MODEL_DEPLOYMENT=gpt-4o-mini
   ```

## Run

```powershell
python .\foundryagent_structureinput_output.py
```

## Notes

- The package entrypoint is `foundryagent_structureinput_output/main.py`.
- The root script now delegates to the package for cleaner module organization.
