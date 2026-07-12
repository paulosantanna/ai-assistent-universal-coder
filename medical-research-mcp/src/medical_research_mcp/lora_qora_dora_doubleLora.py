METHODS={
 "LoRA":{"purpose":"low-rank adaptation","risks":["rank undercapacity","overfitting"]},
 "QLoRA":{"purpose":"quantized-base LoRA","risks":["quantization compatibility","numerical degradation"]},
 "DoRA":{"purpose":"magnitude/direction decomposition","risks":["complexity","library maturity"]},
 "DoubleLoRA":{"purpose":"composed adapters","risks":["interference","evaluation explosion"]},
}
def recommend_adapter(available_vram_gb:float,base_model_billion_parameters:float,comparative_evidence:dict[str,float]|None=None)->dict:
    evidence=comparative_evidence or {}
    choice=max(evidence,key=evidence.get) if evidence else ("QLoRA" if available_vram_gb<base_model_billion_parameters*2 else "LoRA")
    return {"recommendation":choice,"methods":METHODS,"requirement":"Benchmark against retrieval-only and untuned baselines."}
