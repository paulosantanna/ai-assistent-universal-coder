from __future__ import annotations

import logging
from typing import Any

from lsprotocol.types import (
    CallHierarchyOptions,
    CodeActionKind,
    CodeActionOptions,
    CodeLensOptions,
    CompletionOptions,
    DeclarationOptions,
    DefinitionOptions,
    DocumentFilter,
    DocumentFormattingOptions,
    DocumentHighlightOptions,
    DocumentLinkOptions,
    DocumentOnTypeFormattingOptions,
    DocumentRangeFormattingOptions,
    DocumentSymbolOptions,
    ExecuteCommandOptions,
    FoldingRangeOptions,
    HoverOptions,
    ImplementationOptions,
    InlayHintOptions,
    PositionEncodingKind,
    ReferenceOptions,
    RenameOptions,
    SelectionRangeOptions,
    SemanticTokensLegend,
    SemanticTokensOptions,
    ServerCapabilities,
    SignatureHelpOptions,
    TextDocumentSyncKind,
    TextDocumentSyncOptions,
    TypeHierarchyOptions,
    SaveOptions,
    WorkspaceFoldersServerCapabilities,
    WorkspaceOptions,
    FileOperationOptions,
    FileOperationPattern,
    FileOperationFilter,
    FileOperationRegistrationOptions,
    WorkspaceSymbolOptions,
)

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.constants import (
    SERVER_NAME,
    SERVER_VERSION,
    SEMANTIC_TOKEN_TYPES,
    SEMANTIC_TOKEN_MODIFIERS,
)

logger = logging.getLogger(__name__)


def build_server_capabilities(
    config: LSPClientConfig,
) -> ServerCapabilities:
    enable_experimental = config.enable_experimental_features

    capabilities = ServerCapabilities(
        text_document_sync=TextDocumentSyncOptions(
            open_close=True,
            change=TextDocumentSyncKind.Incremental,
            will_save=True,
            will_save_wait_until=False,
            save=SaveOptions(include_text=True),
        ),
        completion_provider=CompletionOptions(
            trigger_characters=["@", ".", "/", "${", "{{", ":", " "],
            all_commit_characters=["\n", "\t"],
            resolve_provider=True,
            work_done_progress=True,
        ),
        hover_provider=HoverOptions(
            work_done_progress=True,
        ),
        signature_help_provider=SignatureHelpOptions(
            trigger_characters=["(", ","],
            retrigger_characters=[")"],
            work_done_progress=True,
        ),
        declaration_provider=DeclarationOptions(),
        definition_provider=DefinitionOptions(),
        implementation_provider=ImplementationOptions(),
        references_provider=ReferenceOptions(
            work_done_progress=True,
        ),
        document_highlight_provider=DocumentHighlightOptions(),
        document_symbol_provider=DocumentSymbolOptions(
            work_done_progress=True,
            label="AEOS Symbols",
        ),
        workspace_symbol_provider=WorkspaceSymbolOptions(
            work_done_progress=True,
        ),
        code_action_provider=CodeActionOptions(
            code_action_kinds=[
                CodeActionKind.QuickFix,
                CodeActionKind.Refactor,
                CodeActionKind.RefactorExtract,
                CodeActionKind.SourceOrganizeImports,
                "aeos.fix.reference",
                "aeos.fix.missing_registration",
                "aeos.fix.schema",
                "aeos.fix.deprecation",
                "aeos.fix.security",
            ],
            resolve_provider=True,
            work_done_progress=True,
        ),
        code_lens_provider=CodeLensOptions(
            resolve_provider=True,
            work_done_progress=True,
        ),
        document_link_provider=DocumentLinkOptions(
            resolve_provider=True,
            work_done_progress=True,
        ),
        color_provider=None,
        document_formatting_provider=DocumentFormattingOptions(),
        document_range_formatting_provider=DocumentRangeFormattingOptions(),
        document_on_type_formatting_provider=DocumentOnTypeFormattingOptions(
            first_trigger_character="\n",
            more_trigger_character=["}", "]"],
        ),
        rename_provider=RenameOptions(
            prepare_provider=True,
            work_done_progress=True,
        ),
        folding_range_provider=FoldingRangeOptions(
            work_done_progress=True,
        ),
        execute_command_provider=ExecuteCommandOptions(
            commands=[
                "aeos.validateDocument",
                "aeos.validateWorkspace",
                "aeos.refreshIndex",
                "aeos.explainDiagnostic",
                "aeos.showDependencyGraph",
                "aeos.showInheritanceGraph",
                "aeos.estimateTokens",
                "aeos.judgeArtifact",
                "aeos.dryRunSkill",
                "aeos.dryRunPlaybook",
                "aeos.previewResolution",
                "aeos.openEvidence",
                "aeos.generateMissingStub",
            ],
            work_done_progress=True,
        ),
        selection_range_provider=SelectionRangeOptions(
            work_done_progress=True,
        ),
        semantic_tokens_provider=SemanticTokensOptions(
            legend=SemanticTokensLegend(
                token_types=SEMANTIC_TOKEN_TYPES,
                token_modifiers=SEMANTIC_TOKEN_MODIFIERS,
            ),
            range=True,
            full=True,
            work_done_progress=True,
        ),
        linked_editing_range_provider=None,
        moniker_provider=None,
        type_hierarchy_provider=TypeHierarchyOptions(
            work_done_progress=True,
        ),
        inlay_hint_provider=InlayHintOptions(
            resolve_provider=True,
            work_done_progress=True,
        ),
        diagnostic_provider=None,
        inline_value_provider=None,
        position_encoding=PositionEncodingKind.Utf16,
        workspace=WorkspaceOptions(
            workspace_folders=WorkspaceFoldersServerCapabilities(
                supported=True,
                change_notifications=True,
            ),
            file_operations=FileOperationOptions(
                did_create=FileOperationRegistrationOptions(
                    filters=[
                        FileOperationFilter(
                            pattern=FileOperationPattern(
                                glob="**/*.{aeos,aeos.yaml,aeos.yml,aeos.json,aeos.toml,md,yaml,yml,json,toml}",
                                matches="file",
                            ),
                        ),
                    ],
                ),
                did_rename=FileOperationRegistrationOptions(
                    filters=[
                        FileOperationFilter(
                            pattern=FileOperationPattern(
                                glob="**/*.{aeos,aeos.yaml,aeos.yml,aeos.json,aeos.toml,md,yaml,yml,json,toml}",
                                matches="file",
                            ),
                        ),
                    ],
                ),
                did_delete=FileOperationRegistrationOptions(
                    filters=[
                        FileOperationFilter(
                            pattern=FileOperationPattern(
                                glob="**/*.{aeos,aeos.yaml,aeos.yml,aeos.json,aeos.toml,md,yaml,yml,json,toml}",
                                matches="file",
                            ),
                        ),
                    ],
                ),
            ),
        ),
        call_hierarchy_provider=CallHierarchyOptions(
            work_done_progress=True,
        ),
    )

    if enable_experimental:
        capabilities.experimental = _build_experimental_capabilities(config)

    return capabilities


def _build_experimental_capabilities(config: LSPClientConfig) -> dict[str, Any]:
    return {
        "enhancedDiagnostics": True,
        "incrementalIndexing": True,
        "realTimeGovernance": True,
        "capabilityNegotiation": True,
        "dependencyVisualization": True,
        "inheritanceGraph": True,
        "tokenEstimation": True,
        "dryRunExecution": True,
        "judgeIntegration": True,
        "evidenceTracking": True,
        "schemaMigrationPreview": True,
        "impactAnalysis": True,
        "configProfiles": True,
        "maxDiagnosticsPerFile": config.max_diagnostics_per_file,
        "maxWorkspaceDiagnostics": config.max_workspace_diagnostics,
        "maxCompletionItems": config.max_completion_items,
        "maxReferences": config.max_references,
        "debounceMilliseconds": config.debounce_milliseconds,
        "indexingConcurrency": config.indexing_concurrency,
        "backgroundIndexing": config.background_indexing,
        "diagnosticProfile": config.diagnostic_profile,
    }


class DynamicRegistrationOptions:
    def __init__(self) -> None:
        pass
