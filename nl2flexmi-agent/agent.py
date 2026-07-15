from smolagents import CodeAgent, ApiModel, LogLevel

from model_types import EClass
import model_tools as mt
import prompts

DEFAULT_REPAIR_PASSES = 3

class ModelAgent:
    def __init__(self, model: ApiModel):
        self.epackage = mt.EPackage(name="default", nsURI="http://cs.york.ac.uk/mmagent/default/1.0", nsPrefix="def")
        self.tools = mt.createTools(self.epackage)
        self.model = model
        self.code_agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            add_base_tools=False,
            verbosity_level=LogLevel.INFO,
            max_steps=20
        )
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_duration = 0
        self.total_repairs = 0

    def run(self, domain_description: str, repair_passes: int = DEFAULT_REPAIR_PASSES):
        self.code_agent.run(prompts.PROMPT_TASK.format(description=domain_description))
        self.increment_metrics()

        # Validate the generated EPackage and do repair passes if there are problems
        for repair_pass in range(DEFAULT_REPAIR_PASSES):
            problems = self.run_post_validation()
            if problems:
                print("Repair pass #{}".format(repair_pass))
                self.code_agent.run(prompts.PROMPT_REPAIR.format(description=domain_description, problems='\n'.join(problems)), additional_args={
                    "generated": self.epackage,
                })
                self.increment_metrics()
                self.total_repairs = repair_pass
            else:
                break

        # Run post-generation repair
        self.run_post_repair()

    def run_post_validation(self) -> list[str]:
        problems = []
        for ec in self.epackage.eClassifiers.values():
            try:
                for sf in ec.eStructuralFeatures.values():
                    if not sf.eType:
                        problems.append('{}.{}: eType not set'.format(ec.name, sf.name))
            except AttributeError:
                # not an eClass
                pass
        return problems

    def run_post_repair(self):
        # Deterministic repair: remove fields already mentioned in a supertype
        for ec in self.epackage.eClassifiers.values():
            try:
                super_names = all_super_feature_names(ec)
                for super_name in super_names:
                    if super_name in ec.eStructuralFeatures:
                        print("Repair: removing {}.{} as it is repeated in a superclass".format(ec.name, super_name))
                        del ec.eStructuralFeatures[super_name]
            except AttributeError:
                # not an EClass
                pass

    def increment_metrics(self):
        self.total_duration += sum(self.code_agent.monitor.step_durations)
        self.total_input_tokens += self.code_agent.monitor.total_input_token_count
        self.total_output_tokens += self.code_agent.monitor.total_output_token_count


def all_super_feature_names(c: EClass) -> set[str]:
    names = set()
    visited = set()
    for eSupertype in c.eSuperTypes:
        all_feature_names(eSupertype, names=names, visited=visited)
    return names

def all_feature_names(c: EClass, names: set[str], visited: set[EClass]):
    if c not in visited:
        visited.add(c)
        for sf_name in c.eStructuralFeatures.keys():
            names.add(sf_name)
        for eSupertype in c.eSuperTypes:
            all_feature_names(eSupertype, names, visited)
