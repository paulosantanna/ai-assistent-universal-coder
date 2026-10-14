<!-- Package: 00_skills/(cloud)/kinghost-clone-site-expert; relative command/resource examples resolve from that package or workspace root. -->

## Completion states

- `PASS`: every FTP-visible path is accounted for and all required integrity checks pass.
- `REVIEW`: clone completed but protocol limitations prevent one or more strong integrity assertions.
- `BLOCKED`: authentication, permissions, ambiguous root or local safety prevents a trustworthy clone.
- `PARTIAL`: one or more expected paths could not be copied; never present this as success.

No successful clone claim is permitted with unexplained missing files.
