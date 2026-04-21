# Changelog

All notable changes to this collection are documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.1.0

- `vyos_cli_config_gen` `interfaces.j2`: render `lacp-rate` on bonding interfaces from `ifc.lacp_rate`, and render `vif` sub-interfaces (address, description, mtu) on bonding interfaces. Previously only `ethernet` supported `vif`, and `lacp-rate` was not emitted at all.
- `vyos_cli_config_gen` `interfaces.j2`: emit bare `set interfaces loopback <name>` declaration for `loopback` type interfaces so they exist in config even with no child properties.
- `vyos_cli_config_gen` `service.j2`: render `set service ssh vrf <name>` from `service.ssh.vrf`.
- `vyos_cli_config_gen` `system.j2`: render `set system option reboot-on-upgrade-failure <n>` from `system.option.reboot_on_upgrade_failure`.
- `vyos_cli_config_gen` `service.j2`: emit `set service dns forwarding name-server <ip>` unquoted (tag node, not leaf) so output matches VyOS canonical form.
- `vyos_cli_config_gen` `service.j2`: emit bare `set service lldp` whenever `service.lldp` is defined so LLDP can be enabled without any child keys, and loosen the outer guard so a scalar `true` works in addition to a dict.
- `vyos_cli_config_gen` `service.j2`: update DHCP server template to VyOS 1.4 syntax. Added `shared_network_name.<name>.description` and `subnet.<subnet>.subnet_id`; moved DHCP options under a new `subnet.<subnet>.option` key (`default_router`, `domain_name`, `name_server` list) — was previously emitted as `default-router`, `dns-server`, `domain-name` directly under subnet (invalid in VyOS 1.4). No consumers currently use these keys.
- `vyos_cli_config_gen` templates: guard bare top-level variable references in `vyos_defined` tests with `| default(none)`. Recent Ansible-core (2.23+) resolves `StrictUndefined` variable references before the test function is invoked, defeating the `UndefinedError` handler in the `vyos_defined` plugin. Affects consumers that don't define `interfaces` or `sysctl_parameter` at any scope. Applied to `interfaces.j2` and `system.j2`.

## 1.0.2

- `vyos_config_deploy_ssh.diff`: strip ANSI escape sequences (e.g. `ESC[m` color resets) from the retrieved running config before diffing. VyOS 1.4's `show configuration commands` leaks terminal escapes into programmatic output on some lines, producing persistent diff noise that looked identical to trailing-whitespace drift.

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
