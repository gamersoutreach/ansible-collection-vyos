# Changelog

All notable changes to this collection are documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.1

- `vyos_config_deploy_ssh.diff`: strip trailing whitespace from the retrieved running config before diffing against the intended config. Works around VyOS 1.4's running-config dump emitting trailing whitespace on certain lines, which produced persistent noise in `make diff` output that survived apply.
- `vyos_sort_config` filter: also rstrip each line defensively, keeping rendered intended config free of trailing whitespace.

## 1.0.0

Initial release.

### Roles

- `vyos_cli_config_gen` — Render VyOS CLI configuration from host/group variables.
- `vyos_config_deploy_ssh` — Deploy rendered configuration to devices via SSH (apply, diff, rollback).

### Plugins

- `vyos_defined` (test) — Test whether a variable is defined, optionally checking value or type.
- `vyos_sort_config` (filter) — Sort VyOS CLI configuration lines to match canonical output order.
