#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Utilities to support running Ansible Playbooks."""

# pylint: disable=invalid-name,dangerous-default-value,unspecified-encoding

import argparse
import io


def replace_inventory_host_ip(
    inv_host_vars_fpath: str, remote_ec2_host_ip: str
) -> None:
    """Replace target host address in Ansible inventory."""
    locale_enc = getattr(io, "LOCALE_ENCODING", None)
    with open(inv_host_vars_fpath, mode="r", encoding=locale_enc) as f:
        lines = f.readlines()
    lines[0] = f"ansible_host: {remote_ec2_host_ip}\n"
    with open(inv_host_vars_fpath, "w", encoding=locale_enc) as f:
        f.writelines(lines)


def replace_inventory_python_version(
    inv_host_vars_fpath: str, python_version: str = "3"
) -> None:
    """Replace target Python path in Ansible inventory."""
    locale_enc = getattr(io, "LOCALE_ENCODING", None)
    with open(inv_host_vars_fpath, mode="r", encoding=locale_enc) as f:
        lines = f.readlines()
    lines[3] = f"ansible_python_interpreter: /usr/bin/python{python_version}\n"
    with open(inv_host_vars_fpath, "w", encoding=locale_enc) as f:
        f.writelines(lines)


def show_file_contents(inv_host_vars_filepath: str) -> None:
    """Show contents of a text file."""
    locale_enc = getattr(io, "LOCALE_ENCODING", None)
    with open(inv_host_vars_filepath, mode="r", encoding=locale_enc) as f:
        lines = lines = f.readlines()
    for line in lines:
        print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--python-version",
        type=str,
        dest="python_version",
        default="2.7",
        help="remote version of python",
    )
    args = parser.parse_args()

    inventory_host_vars_filepath = "inventories/production/host_vars/ec2host"

    replace_inventory_python_version(
        inventory_host_vars_filepath, args.python_version
    )
    show_file_contents(inventory_host_vars_filepath)
