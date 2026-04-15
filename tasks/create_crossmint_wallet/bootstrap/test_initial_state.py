import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


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
        f"@crossmint/wallets-sdk is not installed or not importable: {result.stderr}"
    )


def test_wallet_result_not_yet_created():
    wallet_result = os.path.join(HOME_DIR, "wallet_result.json")
    assert not os.path.isfile(wallet_result), (
        f"wallet_result.json already exists at {wallet_result} — it should not exist before the task."
    )


def test_create_wallet_script_not_yet_created():
    script_path = os.path.join(HOME_DIR, "create_wallet.js")
    assert not os.path.isfile(script_path), (
        f"create_wallet.js already exists at {script_path} — it should be created by the agent."
    )
