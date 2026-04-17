# gamersoutreach.vyos

Reusable Ansible roles and plugins for managing VyOS 1.4 devices.

Inspired by the [Arista Validated Design](https://avd.sh/en/stable/) generate-then-deploy pattern. This collection is consumed by multiple internal network projects.

## Contents

### Roles

- **`gamersoutreach.vyos.vyos_cli_config_gen`** — Renders VyOS CLI configuration from host/group variables using Jinja2 templates. Covers firewall, high-availability, interfaces, load-balancing, NAT, policy, protocols (BGP/OSPF/static), QoS, service, system, VPN, and VRF sections. Output is written to `{{ playbook_dir }}/configs/intended/<hostname>.cfg`.
- **`gamersoutreach.vyos.vyos_config_deploy_ssh`** — Deploys rendered configuration to VyOS devices over SSH via `vyos.vyos.vyos_config`. Provides `main.yml` (apply), `diff.yml`, and `rollback.yml` task files. Backs up pre- and post-apply running configs to `{{ playbook_dir }}/configs/backup/`.

### Plugins

- **`gamersoutreach.vyos.vyos_defined`** (test) — Tests whether a variable is defined, not `None`, and optionally matches a specific value or type. Replacement for `arista.avd.defined`.

  ```jinja2
  {% if x is gamersoutreach.vyos.vyos_defined %}
  {% if x is gamersoutreach.vyos.vyos_defined(true) %}
  {% if x is gamersoutreach.vyos.vyos_defined(var_type="dict") %}
  ```

  Because Ansible's `StrictUndefined` raises on missing dict keys before tests evaluate, guard dotted accesses with `| default(none)`:

  ```jinja2
  {% if (firewall.group | default(none)) is gamersoutreach.vyos.vyos_defined %}
  ```

- **`gamersoutreach.vyos.vyos_sort_config`** (filter) — Sorts generated config lines to match VyOS's canonical output order (IP-aware sorting for unquoted path nodes, string sorting for quoted leaf values). Applied automatically at the end of `vyos_cli_config_gen`.

## Installation

Add to `collections/requirements.yml` in the consuming project:

```yaml
---
collections:
  - name: gamersoutreach.vyos
    source: https://github.com/gamersoutreach/ansible-collection-vyos.git
    type: git
    version: 0.1.0
```

Install:

```
ansible-galaxy collection install -r collections/requirements.yml -p ./collections
```

`vyos.vyos` is declared as a transitive dependency and will be installed automatically.

## Usage

```yaml
---
- name: Generate intended configuration
  hosts: all
  gather_facts: false
  roles:
    - gamersoutreach.vyos.vyos_cli_config_gen

- name: Apply intended configuration
  hosts: all
  gather_facts: false
  connection: ansible.netcommon.network_cli
  roles:
    - gamersoutreach.vyos.vyos_cli_config_gen
    - gamersoutreach.vyos.vyos_config_deploy_ssh
```

For diff and rollback, include specific task files:

```yaml
tasks:
  - name: Include diff tasks
    ansible.builtin.include_role:
      name: gamersoutreach.vyos.vyos_config_deploy_ssh
      tasks_from: diff

  - name: Include rollback tasks
    ansible.builtin.include_role:
      name: gamersoutreach.vyos.vyos_config_deploy_ssh
      tasks_from: rollback
```

## Variables

The `vyos_cli_config_gen` role consumes top-level variables whose keys map directly to Jinja2 template sections. Variable names use underscores which become hyphens in VyOS CLI (e.g., `default_action` -> `default-action`).

Top-level keys consumed:

- `firewall`, `high_availability`, `interfaces`, `load_balancing`, `nat`, `policy`, `protocols`, `qos`, `service`, `system`, `vpn`, `vrf`

### Conventions

- **Dict keyed by name** — named collections (firewall rulesets, prefix lists, zones, interfaces by type)
- **Dict keyed by number** — numbered rules within a collection
- **List of dicts** — items with an identifying field (BGP neighbors)
- **Simple list** — flat value lists (addresses, name servers)
- **Boolean flags** — set to `true` to output the flag, omit or `false` to suppress

### Quoting rules (matched by templates)

- **Quoted** (single quotes): leaf values — `description 'text'`, `port '22'`, `state 'established'`
- **Unquoted**: path node keys — `next-hop 10.0.0.1`, `interface eth0`, `network 10.0.0.0/24`
- **No value**: boolean flags — `blackhole`, `disable`, `enable-default-log`

## Role Variables

### `vyos_cli_config_gen`

| Variable                              | Default                                               | Description               |
| ------------------------------------- | ----------------------------------------------------- | ------------------------- |
| `vyos_cli_config_gen_root_dir`        | `{{ playbook_dir }}`                                  | Root for generated output |
| `vyos_cli_config_gen_config_dir_name` | `configs/intended`                                    | Output directory name     |
| `vyos_cli_config_gen_config_dir`      | `{{ vyos_cli_config_gen_root_dir }}/configs/intended` | Full output path          |

### `vyos_config_deploy_ssh`

| Variable                                                | Default                                                  | Description                             |
| ------------------------------------------------------- | -------------------------------------------------------- | --------------------------------------- |
| `vyos_config_deploy_ssh_root_dir`                       | `{{ playbook_dir }}`                                     | Root for output structure               |
| `vyos_config_deploy_ssh_config_dir`                     | `{{ vyos_config_deploy_ssh_root_dir }}/configs/intended` | Where intended config is read from      |
| `vyos_config_deploy_ssh_config_diff_dir`                | `{{ vyos_config_deploy_ssh_root_dir }}/configs/diff`     | Where running config is staged for diff |
| `vyos_config_deploy_ssh_pre_running_config_backup_dir`  | `{{ vyos_config_deploy_ssh_root_dir }}/configs/backup`   | Pre-apply backup path                   |
| `vyos_config_deploy_ssh_post_running_config_backup_dir` | `{{ vyos_config_deploy_ssh_root_dir }}/configs/backup`   | Post-apply backup path                  |

## Development

To iterate on this collection from a consuming project without pushing changes, the consuming project's Makefile _may_ accept an optional bind mount pointing at a local checkout. Export `VYOS_COLLECTION_DEV` before running `make plan`, and the bind mount will shadow the installed collection for the duration of the run.

```
export VYOS_COLLECTION_DEV=/path/to/ansible-collection-vyos
make plan
```

## License

MIT — see [LICENSE](LICENSE).
