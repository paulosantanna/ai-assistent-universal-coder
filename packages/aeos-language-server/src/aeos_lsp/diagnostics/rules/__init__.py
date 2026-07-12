from aeos_lsp.diagnostics.rules.agents import AgentNotRegisteredRule
from aeos_lsp.diagnostics.rules.architecture import ArchitectureViolationRule
from aeos_lsp.diagnostics.rules.cycles import (
    AgentInheritanceCycleRule,
    DependencyCycleRule,
    PlaybookCycleRule,
    SkillCycleRule,
)
from aeos_lsp.diagnostics.rules.dangling_references import (
    AmbiguousReferenceRule,
    DanglingReferenceRule,
)
from aeos_lsp.diagnostics.rules.deprecations import DeprecatedFieldRule
from aeos_lsp.diagnostics.rules.duplicate_ids import DuplicateIdRule
from aeos_lsp.diagnostics.rules.evidence import (
    ArtifactProvenanceRule,
    EvidenceGateRule,
    EvidenceHashRule,
    PassWithoutEvidenceRule,
)
from aeos_lsp.diagnostics.rules.inheritance import InvalidInheritanceRule
from aeos_lsp.diagnostics.rules.judge import ImpossibleScoreRule, InconsistentJudgeRule
from aeos_lsp.diagnostics.rules.models import ModelCompatibilityRule
from aeos_lsp.diagnostics.rules.paths import PathEscapeRule
from aeos_lsp.diagnostics.rules.permissions import (
    IncompatiblePermissionRule,
    MissingPermissionRule,
)
from aeos_lsp.diagnostics.rules.playbooks import (
    PlaybookNotRegisteredRule,
    StepWithoutExecutorRule,
    UnreachableStepRule,
)
from aeos_lsp.diagnostics.rules.policies import PolicyDeniesOperationRule
from aeos_lsp.diagnostics.rules.registries import (
    DuplicateRegistryRule,
    MultipleSourcesOfTruthRule,
)
from aeos_lsp.diagnostics.rules.retries import UnlimitedRetryRule
from aeos_lsp.diagnostics.rules.rollback import MutatingStepWithoutRollbackRule
from aeos_lsp.diagnostics.rules.schema import InvalidSchemaRule
from aeos_lsp.diagnostics.rules.security import (
    CommandInjectionRule,
    InsecureShellCommandRule,
)
from aeos_lsp.diagnostics.rules.skills import SkillNotRegisteredRule
from aeos_lsp.diagnostics.rules.syntax import InvalidSyntaxRule
from aeos_lsp.diagnostics.rules.timeouts import MissingTimeoutRule
from aeos_lsp.diagnostics.rules.token_budget import (
    ContextWindowIncompatibleRule,
    EstimateAboveBudgetRule,
    InvalidBudgetRule,
)
from aeos_lsp.diagnostics.rules.tools import ToolNotRegisteredRule

ALL_RULES = [
    InvalidSyntaxRule(),
    InvalidSchemaRule(),
    DuplicateIdRule(),
    DanglingReferenceRule(),
    AmbiguousReferenceRule(),
    AgentInheritanceCycleRule(),
    PlaybookCycleRule(),
    SkillCycleRule(),
    DependencyCycleRule(),
    InvalidInheritanceRule(),
    AgentNotRegisteredRule(),
    SkillNotRegisteredRule(),
    ToolNotRegisteredRule(),
    PlaybookNotRegisteredRule(),
    UnreachableStepRule(),
    StepWithoutExecutorRule(),
    MissingPermissionRule(),
    IncompatiblePermissionRule(),
    PolicyDeniesOperationRule(),
    EvidenceGateRule(),
    PassWithoutEvidenceRule(),
    ArtifactProvenanceRule(),
    EvidenceHashRule(),
    InconsistentJudgeRule(),
    ImpossibleScoreRule(),
    InvalidBudgetRule(),
    EstimateAboveBudgetRule(),
    ContextWindowIncompatibleRule(),
    ModelCompatibilityRule(),
    PathEscapeRule(),
    InsecureShellCommandRule(),
    CommandInjectionRule(),
    MutatingStepWithoutRollbackRule(),
    MissingTimeoutRule(),
    UnlimitedRetryRule(),
    DuplicateRegistryRule(),
    MultipleSourcesOfTruthRule(),
    ArchitectureViolationRule(),
    DeprecatedFieldRule(),
]


def register_all_rules(registry: object) -> None:
    from aeos_lsp.diagnostics.registry import DiagnosticRuleRegistry

    if isinstance(registry, DiagnosticRuleRegistry):
        registry.register_all(ALL_RULES)
