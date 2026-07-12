from dataclasses import dataclass,asdict
@dataclass
class LearningCandidate:
    id:str; observation:str; evidence:list[str]; applicability:list[str]; limitations:list[str]; status:str="CANDIDATE"
def evaluate_candidate(c:LearningCandidate)->dict:
    problems=[]
    if not c.evidence: problems.append("missing evidence")
    if not c.applicability: problems.append("missing applicability")
    if not c.limitations: problems.append("missing limitations")
    return {"candidate":asdict(c),"eligible_for_review":not problems,"problems":problems,
      "next_status":"UNDER_REVIEW" if not problems else "REJECTED"}
def promotion_chain()->list[str]:
    return ["OBSERVATION","EVIDENCE","FINDING","CANDIDATE_LESSON","INDEPENDENT_VALIDATION","PROMOTED_KNOWLEDGE","REVALIDATION_OR_DEPRECATION"]
