# MSFoundryStructureInputOutput

A minimal Python demo showing how to use **Structured Input** and **Structured Output** with a **Microsoft Foundry Agent**, built on the `azure-ai-projects` (2.x) SDK and the OpenAI Responses protocol.

The sample creates a Foundry agent that extracts order details from a JSON payload and returns the result strictly validated against a schema — no free-form text, no manual parsing.

## What this demonstrates

1. **Structured Output** — The agent's reply is constrained to a JSON Schema (generated from a Pydantic model) so the response always matches a known shape. Because the schema is enforced at the API level, there's no risk of missing fields, wrong types, or hallucinated keys.

2. **Structured Input** — Instead of sending a loose natural-language sentence, the caller sends a well-defined JSON object as the input. This makes extraction deterministic on the way in, not just on the way out.

Together, this pattern turns an LLM agent into a predictable, typed function you can call from regular application code.

## How it works

- An agent is created (or versioned) in your Foundry project using `PromptAgentDefinition`.
- The desired output shape is defined once as a Pydantic model (`OrderInfo`) and converted to a strict JSON Schema.
- That schema is attached to the agent definition's `text` field at creation time. **This is important**: once you call a model through an `agent_reference`, the response format is fixed by the agent's own definition — it can't be overridden per-request.
- At call time, the script sends a JSON payload as input and gets back JSON guaranteed to match `OrderInfo`, which is then parsed straight into a typed Python object.

## Prerequisites

- Python 3.10+
- An Azure subscription with a [Microsoft Foundry project](https://learn.microsoft.com/azure/ai-foundry/) and a deployed chat model (e.g. `gpt-4o-mini`)
- The [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed and you're logged in (`az login`)
- Appropriate role assignment on the Foundry project resource (Azure AI Developer role or similar) for your signed-in identity

## Installation

```bash
git clone https://github.com/praveen11singh/MSFoundryStructureInputOutput.git
cd MSFoundryStructureInputOutput

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install azure-ai-projects azure-identity pydantic openai --upgrade
```

## Configuration

Set the following environment variables before running the script:

| Variable            | Description                                                                                     | Example |
|---------------------|---------------------------------------------------------------------------------------------------|---------|
| `PROJECT_ENDPOINT`  | Your Foundry project endpoint (found on the project's Overview page)                              | `https://my-resource.services.ai.azure.com/api/projects/my-project` |
| `MODEL_DEPLOYMENT`  | The name of a model deployment in your Foundry project (defaults to `gpt-4o-mini` if not set)     | `gpt-4o-mini` |

On PowerShell:

```powershell
$env:PROJECT_ENDPOINT = "https://my-resource.services.ai.azure.com/api/projects/my-project"
$env:MODEL_DEPLOYMENT = "gpt-4o-mini"
```

On bash/zsh:

```bash
export PROJECT_ENDPOINT="https://my-resource.services.ai.azure.com/api/projects/my-project"
export MODEL_DEPLOYMENT="gpt-4o-mini"
```

Alternatively, use a `.env` file with `python-dotenv` and add `load_dotenv()` near the top of the script.

## Usage

```bash
python foundryagent_structureinput_output.py
```

Example output:

```
Agent ready (name: order-extractor-agent, version: 1)

Raw JSON returned by the agent:
{"customer_name":"Jordan Lee","product":"Wireless Mouse","quantity":3,"unit_price_usd":24.99,"total_usd":74.97,"priority":"expedited"}

Parsed into a typed Python object:
customer_name='Jordan Lee' product='Wireless Mouse' quantity=3 unit_price_usd=24.99 total_usd=74.97 priority='expedited'

Total charge: $74.97 (expedited)
```

## Project structure

```
MSFoundryStructureInputOutput/
├── foundryagent_structureinput_output.py   # Main demo script
└── README.md                               # This file
```

## Notes

- Each run calls `agents.create_version(...)`, which creates a new version of the agent rather than mutating an existing one in place. Expect the version number to increment on every run. If you'd rather reuse an existing version, check for it first and only call `create_version` when it doesn't exist.
- This sample targets the newer **Foundry projects (v2) API** (`azure-ai-projects` 2.x). If you're using the older `azure-ai-agents` thread/run-based SDK, the agent creation and invocation calls differ (`create_agent`, `threads`, `runs`, etc.) — this repo does not cover that API surface.
- Authentication uses `DefaultAzureCredential`, which is convenient for local development. For production, use a specific credential (e.g. `ManagedIdentityCredential`) instead.

## References

- [Microsoft Foundry Agents overview](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Structured outputs with Azure OpenAI in Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/structured-outputs)
- [Customize agent behavior at runtime with structured inputs](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/structured-inputs)

## License

Open Sourced
