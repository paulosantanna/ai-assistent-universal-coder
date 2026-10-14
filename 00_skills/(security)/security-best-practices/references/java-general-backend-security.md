# Java backend security

Updated: 2026-10-13
Entry point: ../SKILL.md. Read for any Java backend. Source: IMG_2740–IMG_2748; consult official docs for the actual JDK/library version.

- Trace request/event input into SQL, process arguments, filesystem, URL and deserialization. Parameterize values; allowlist dynamic identifiers and commands. Never assemble executable SQL or shell from untrusted strings.
- Resolve filesystem paths against an authorized base, account for symlinks and check the final target before reading/writing. Treat filenames and archive entries as untrusted.
- Avoid deserializing arbitrary native Java objects. If the application requires it, inspect explicit type/depth/size filters and exposure. Jackson polymorphic configuration requires a proven allowed-type boundary.
- XML parsers: disable external entity/DTD resolution where unneeded; prove actual parser settings. Deny attacker-controlled external resources rather than assuming framework defaults cover every parser.
- Secrets use runtime providers. Crypto uses verified modern authenticated encryption, secure randomness and managed key/nonce handling; do not prescribe a mode without its nonce/authentication contract.
- Bound payload size, memory, retries and concurrency. Validate identifiers and tenant/object access in the actual trust boundary. No log of tokens, credentials, personal identifiers or full payloads by default.
- Output finding only with reachable flow and missing control. Existing static scanners are evidence to inspect, not a substitute for behavior or a reason to ignore an evident risk.

Normative source: [Oracle Secure Coding Guidelines](https://www.oracle.com/java/technologies/javase/seccodeguide.html). Confirm the exact platform/library documentation at execution; this module is not live CVE truth.
