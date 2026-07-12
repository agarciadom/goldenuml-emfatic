import os

import dotenv
from smolagents import LiteLLMModel

from agent import ModelAgent
import prompts

def main(agent: ModelAgent, domain_description: str):
    agent.execute(prompts.PROMPT_TASK.format(description=domain_description))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog="ModelAgent",
        description="Domain-specific model agent for Ecore metamodels"
    )
    parser.add_argument("-m", "--model")
    parser.add_argument("-b", "--api-base")
    parser.add_argument("-k", "--api-key")
    parser.add_argument("filename", help="File with the description of the domain")
    args = parser.parse_args()
    dotenv.load_dotenv()

    agent = ModelAgent(
        model=LiteLLMModel(
            model_id=args.model or os.getenv("MODEL_NAME"),
            api_base=args.api_base or os.getenv('API_BASE', "http://localhost:11434"),
            api_key=args.api_key or os.getenv('API_KEY', "ollama"),
        )
    )

    with open(args.filename) as f:
        main(agent, f.read())