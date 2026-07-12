from .models import Status,ValidationReport,ValidationCriterion
def validate_10_0(criteria:list[ValidationCriterion])->ValidationReport:
    if not criteria:return ValidationReport(score=0,accepted=False,status=Status.BLOCKED,criteria=[],blocking_reasons=["No criteria"])
    total=sum(c.weight for c in criteria); achieved=sum(c.weight for c in criteria if c.passed and c.evidence)
    score=round(10*achieved/total,2)
    failures=[f"{c.id}: {c.reason or 'failed or lacks evidence'}" for c in criteria if c.mandatory and (not c.passed or not c.evidence)]
    accepted=score==10 and not failures and all(c.passed and c.evidence for c in criteria)
    return ValidationReport(score=score,accepted=accepted,status=Status.PASS if accepted else Status.REWORK_REQUIRED,
    criteria=criteria,blocking_reasons=failures)
