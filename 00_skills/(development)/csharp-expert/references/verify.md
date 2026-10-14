# Verify

Updated: 2026-10-09

Run these from the directory of the project that changed. A non-zero exit blocks a done claim.

1. `dotnet build` the project that contains the change.
2. `dotnet test` when that project, or a test project that already references it, contains tests for the behavior. Pass that project path. Do not add a test project unless the user asked for tests.
3. Report the command and the exit code.

`dotnet` missing: stop. Do not claim the code compiles.

Warnings the project treats as errors fail the build. Fix those in the lines this change owns. Leave unrelated warnings.

A green build of a different TFM is not proof for the TFM that was edited.
