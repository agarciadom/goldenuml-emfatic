from smolagents import CodeAgent, ApiModel, LogLevel

import model_tools as mt

class ModelAgent:
    def __init__(self, model: ApiModel):
        self.epackage = mt.EPackage(name="default", nsURI="http://cs.york.ac.uk/mmagent/default/1.0")
        self.tools = mt.createTools(self.epackage)
        self.model = model

    def execute(self, task):
        code_agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            add_base_tools=False,
            verbosity_level=LogLevel.INFO,
            max_steps=20
        )
        code_agent.run(task)
