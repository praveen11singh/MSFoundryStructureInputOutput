import json

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

from .config import AGENT_NAME, MODEL_DEPLOYMENT, PROJECT_ENDPOINT
from .schemas import OrderInfo, to_strict_json_schema


def get_project_client() -> AIProjectClient:
    credential = DefaultAzureCredential()
    return AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)


def create_agent(project: AIProjectClient):
    return project.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL_DEPLOYMENT,
            instructions=(
                "You extract order details from the JSON the user sends and "
                "return them strictly according to the response schema. "
                "Compute total_usd as quantity * unit_price_usd."
            ),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "OrderInfo",
                    "schema": to_strict_json_schema(OrderInfo),
                    "strict": True,
                }
            },
        ),
    )


def call_agent(openai_client, agent, structured_request: dict):
    return openai_client.responses.create(
        input=json.dumps(structured_request),
        extra_body={"agent_reference": {"type": "agent_reference", "name": agent.name}},
    )
