from .subagents import create_tasks
PHASES=["BASELINE","REPOSITORY_DISCOVERY","ARCHITECTURE_DATA_FLOW","SOURCE_GOVERNANCE","DATA_PROVENANCE",
"RAG_BM25","ADAPTER_TRAINING","CONTINUOUS_LEARNING","SIMULATION","EXTERNAL_TRIAL_VALIDATION",
"OWASP_SUPPLY_CHAIN","CONTROLLED_REFACTOR","DOCUMENTATION","BETA_READINESS"]
def create_complete_plan(repository:str,disease:str,token_budget:int=60000)->dict:
    objective=f"Audit and evolve {repository} into a research-only Beta for {disease}"
    return {"objective":objective,"phases":PHASES,"subagent_tasks":create_tasks(objective,token_budget),
    "completion_rule":"All mandatory expert-validator criteria pass with evidence.",
    "clinical_boundary":"Laboratory, animal and human research remain externally controlled."}
