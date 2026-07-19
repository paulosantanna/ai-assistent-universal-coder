# Spec-Driven Delivery

## Preconditions

- Specification validates without errors.
- Every requirement is linked to at least one acceptance criterion.
- Human approval references the current normative SHA-256.

## Execution

1. Create or update the structured specification.
2. Validate requirements and traceability.
3. Record explicit approval and evidence reference.
4. Lock the normative surface and start implementation.
5. Optionally trigger the allowlisted `spec-driven-delivery` N8N workflow.
6. Run tests, inspections and metrics declared by each criterion.
7. Record immutable evidence references.
8. Accept only when every criterion passes and approval remains current.

## Failure Policy

Failed evidence rejects the specification. Normative changes return it to draft and require re-approval.
