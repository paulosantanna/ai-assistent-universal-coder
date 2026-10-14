<!-- Package: 00_skills/(cloud)/kinghost-expert; relative command/resource examples resolve from that package or workspace root. -->

## Executable dependencies

- `kinghost-control`: cookie panel session, domains, credentials, FTP, MySQL, clone, production FSM, knowledge.
- governed `browser`/Playwright: panel-only tools such as DNS, SSL, backup request, antivirus, WAF, e-mail, Varnish/performance, Git integration and resource creation.
- `wordpress-expert`: WordPress themes/plugins/blocks/content and WordPress production engineering.
- `kinghost-commerce`: only when SSH/SFTP/Postgres commerce sessions are the safer documented protocol.
- `runtime-auth` / `runtime-http`: extra authenticated runtime sessions without exposing secrets.

### Compatibility contract

Existing integrations remain stable while the hosting surface expands:

- bind **already created** FTP/MySQL/WordPress identities as opaque runtime references; never rediscover their passwords;
- use `kinghost_control.site.clone` for governed site clone planning/execution;
- use `kinghost_control.ftp.tree.upload` for governed FTP publication under mutation gates;
- preserve playbook id `kinghost-wordpress-publish` and command `npm run aeos:kinghost:publish` for the one-command WordPress publish path;
- keep `domain.list` / `domain.select` as the canonical domain-selection contract.
