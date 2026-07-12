ARCHITECTURE={
 "immutable_history":"Supersede or deprecate; never erase evidence.",
 "replay_buffer":"Test new candidates against historical and edge cases.",
 "shadow_promotion":"Candidates remain in shadow mode.",
 "drift":"Monitor data, retrieval, model, calibration and subgroup drift.",
 "rollback":"Every promoted artifact is reversible.",
 "human_control":"No autonomous clinical behavior changes.",
}
def continuous_learning_gate(capabilities:list[str])->dict:
    required={"versioned_data","versioned_models","replay_suite","drift_detection","shadow_mode","approval_gate","rollback"}
    missing=sorted(required-set(capabilities))
    return {"passed":not missing,"missing":missing,"architecture":ARCHITECTURE}
