"""
Jinja2 filter plugin: vyos_sort_config

Sorts VyOS CLI configuration lines to match the canonical order
produced by VyOS. Delete lines remain at the top, followed by
set lines sorted to match VyOS's ordering rules:

- Unquoted path components (node keys): IP addresses and numbers
  are sorted numerically.
- Quoted leaf values: sorted as strings (alphabetical).
"""

from __future__ import annotations

import ipaddress


def _parse_numeric(value):
    """Try to parse as IP network, IP address, or integer. Returns sort tuple or None."""
    if "/" in value:
        try:
            net = ipaddress.ip_network(value, strict=False)
            return (0, int(net.network_address), net.prefixlen)
        except ValueError:
            pass
    try:
        return (0, int(ipaddress.ip_address(value)), 0)
    except ValueError:
        pass
    try:
        return (1, int(value), 0)
    except ValueError:
        pass
    return None


def _sort_key(line):
    """Generate a sort key that matches VyOS canonical ordering."""
    parts = line.split()
    key = []
    for part in parts:
        if part.startswith("'") and part.endswith("'"):
            # Quoted leaf value — sort as string
            key.append((2, part, 0))
        else:
            # Unquoted path component — try numeric/IP parsing
            parsed = _parse_numeric(part)
            if parsed is not None:
                key.append(parsed)
            else:
                key.append((2, part, 0))
    return key


def vyos_sort_config(config_text):
    """Sort VyOS CLI config: delete lines first, then set lines in VyOS canonical order."""
    lines = [line.rstrip() for line in config_text.strip().split("\n")]
    delete_lines = [line for line in lines if line.startswith("delete ")]
    set_lines = [line for line in lines if line.startswith("set ")]
    return "\n".join(delete_lines + sorted(set_lines, key=_sort_key))


class FilterModule:
    """Ansible filter plugin entry point."""

    def filters(self):
        return {
            "vyos_sort_config": vyos_sort_config,
        }
