<!-- Package: 00_skills/(development)/solve-problems; relative command/resource examples resolve from that package or workspace root. -->

## 13. Stop conditions

Stop when:

- the affected code cannot be located;
- the language cannot be identified with repository evidence;
- required project memory is unavailable and the change would be high risk without it;
- the fix requires architecture or structure changes;
- the only viable fix requires comments in source code;
- the change would leave orphan variables, unused imports or dead code;
- the required test suite cannot run and no approved risk deferral exists;
- pod logs or telemetry are required to diagnose the problem but are unavailable;
- approval is required for mutation, dependency, destructive action, credential access or production behavior;
- the honest evaluator returns `BLOCKED`;
- verification fails after the scoped fix.
