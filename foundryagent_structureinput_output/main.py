from .agent import call_agent, create_agent, get_project_client
from .schemas import OrderInfo


def main() -> None:
    project = get_project_client()
    agent = create_agent(project)
    print(f"Agent ready (name: {agent.name}, version: {agent.version})")

    openai_client = project.get_openai_client()
    structured_request = {
        "customer_name": "Jordan Lee",
        "items": [{"product": "Wireless Mouse", "quantity": 3, "unit_price_usd": 24.99}],
        "shipping": "expedited",
    }

    response = call_agent(openai_client, agent, structured_request)
    raw_json = response.output_text
    order = OrderInfo.model_validate_json(raw_json)

    print("\nRaw JSON returned by the agent:")
    print(raw_json)
    print("\nParsed into a typed Python object:")
    print(order)
    print(f"\nTotal charge: ${order.total_usd:.2f} ({order.priority})")


if __name__ == "__main__":
    main()
