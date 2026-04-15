import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist."


def test_crossmint_wallets_sdk_installed():
    result = subprocess.run(
        ["node", "-e", "require('@crossmint/wallets-sdk')"],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
    )
    assert result.returncode == 0, (
        f"@crossmint/wallets-sdk is not installed: {result.stderr}"
    )


def test_transfer_script_not_yet_created():
    script_path = os.path.join(HOME_DIR, "transfer_usdc.js")
    assert not os.path.isfile(script_path), (
        f"transfer_usdc.js already exists — should be created by the agent."
    )


def test_transfer_log_not_yet_created():
    log_path = os.path.join(HOME_DIR, "transfer_log.json")
    assert not os.path.isfile(log_path), (
        f"transfer_log.json already exists — should not exist before the task."
    )
