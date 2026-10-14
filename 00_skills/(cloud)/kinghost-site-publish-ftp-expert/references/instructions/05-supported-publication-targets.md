<!-- Package: 00_skills/(cloud)/kinghost-site-publish-ftp-expert; relative command/resource examples resolve from that package or workspace root. -->

## Supported publication targets

### PHP site

May publish application code, public assets and approved runtime files under the selected remote root. Runtime-specific configuration must be validated separately against KingHost PHP capability and current application requirements.

### WordPress site

Default allowed publication scope is custom application content such as:

- `wp-content/themes/<approved-theme>`;
- `wp-content/plugins/<approved-plugin>`;
- approved `wp-content/mu-plugins`;
- static assets/uploads only when explicitly part of the change.

Default protected paths:

- `wp-config.php`;
- `.env` and secret-bearing config;
- `wp-admin/`;
- `wp-includes/`;
- WordPress core files;
- database dumps;
- server/private keys.

Protected paths require an explicit high-risk scope and owning-skill approval; ordinary feature publication must not touch them.
