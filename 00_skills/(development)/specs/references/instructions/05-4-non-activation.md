<!-- Package: 00_skills/(development)/specs; relative command/resource examples resolve from that package or workspace root. -->

## 4. Non-activation

Do not activate when:

- the request is pure read-only inspection and produces no durable artifact;
- the user asks only a small factual question;
- the work is an emergency stop or safety containment action where delaying for a spec would increase harm;
- the current turn is already executing `specs`;
- a valid, current `specs` evidence reference is already attached to the downstream skill request.
