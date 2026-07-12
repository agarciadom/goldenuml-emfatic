from smolagents import CodeAgent, ApiModel, LogLevel, RunResult

import model_tools as mt
import prompts

class ModelAgent:
    def __init__(self, model: ApiModel):
        self.epackage = mt.EPackage(name="default", nsURI="http://cs.york.ac.uk/mmagent/default/1.0", nsPrefix="def")
        self.tools = mt.createTools(self.epackage)
        self.model = model

    def run(self, domain_description: str):
        code_agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            add_base_tools=False,
            verbosity_level=LogLevel.INFO,
            max_steps=20
        )
        code_agent.run(prompts.PROMPT_TASK.format(description=domain_description))

        # Validate the generated EPackage and report any issues
        problems = []
        for ec in self.epackage.eClassifiers.values():
            try:
                for sf in ec.eStructuralFeatures.values():
                    if not sf.eType:
                        problems.append('{}.{}: eType not set'.format(ec.name, sf.name))
            except AttributeError:
                # not an eClass
                pass

        # Do one repair pass
        if problems:
            code_agent.run(prompts.PROMPT_REPAIR.format(description=domain_description, problems='\n'.join(problems)), additional_args={
                "generated": self.epackage,
            })