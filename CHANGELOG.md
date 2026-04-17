# Changelog

All notable changes to this collection are documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0

Initial release.

### Roles

- `vyos_cli_config_gen` — Render VyOS CLI configuration from host/group variables.
- `vyos_config_deploy_ssh` — Deploy rendered configuration to devices via SSH (apply, diff, rollback).

### Plugins

- `vyos_defined` (test) — Test whether a variable is defined, optionally checking value or type.
- `vyos_sort_config` (filter) — Sort VyOS CLI configuration lines to match canonical output order.
