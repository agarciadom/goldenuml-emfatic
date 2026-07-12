import csv
import os
import typing

import dotenv
from smolagents import LiteLLMModel

from agent import ModelAgent

def main(agent: ModelAgent, domain_description: str, output_file: typing.TextIO, csv_path: str, model_id: str):
    agent.run(domain_description)
    agent.epackage.write_to_file(output_file)
    if csv_path:
        with open(csv_path, 'w') as csvfile:
            monitor = agent.code_agent.monitor
            writer = csv.writer(csvfile)
            writer.writerow(['model_id', 'total_duration_seconds', 'total_input_tokens', 'total_output_tokens'])
            writer.writerow([model_id, agent.total_duration, agent.total_input_tokens, agent.total_output_tokens])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog="ModelAgent",
        description="Domain-specific model agent for Ecore metamodels"
    )
    parser.add_argument("-m", "--model")
    parser.add_argument("-b", "--api-base")
    parser.add_argument("-k", "--api-key")
    parser.add_argument("-s", "--stats", help="Path to CSV stats file")
    parser.add_argument("input_filename", help="File with the description of the domain")
    parser.add_argument("output_filename", help="Destination path for the Flexmi output")
    args = parser.parse_args()
    dotenv.load_dotenv()

    model_id = args.model or os.getenv("MODEL_NAME")
    agent = ModelAgent(
        model=LiteLLMModel(
            model_id=model_id,
            api_base=args.api_base or os.getenv('API_BASE', "http://localhost:11434"),
            api_key=args.api_key or os.getenv('API_KEY', "ollama"),
        )
    )

    with open(args.input_filename) as f:
        with open(args.output_filename, "w") as output_f:
            main(agent, f.read(), output_f, csv_path=args.stats, model_id=model_id)