<!-- Package: 00_skills/(cloud)/kinghost-clone-site-expert; relative command/resource examples resolve from that package or workspace root. -->

## Mission

Clone an authorized KingHost-hosted site from FTP into a controlled workspace as completely and reproducibly as the selected FTP account permits, preserving directory structure, filenames, binary payloads and evidence of transfer integrity while never mutating the remote source.

This skill means **absolute clone of the FTP-visible site tree**. It must not falsely claim that FTP alone contains database rows, mailbox data, DNS, panel settings, cron configuration or secrets. For WordPress/PHP sites that also require database state, delegate the data portion to `kinghost-database-expert` / `kinghost-backup-recovery-expert` and report the combined result explicitly.
