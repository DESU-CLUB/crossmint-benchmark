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


def test_sign_script_not_yet_created():
    script_path = os.path.join(HOME_DIR, "sign_message.js")
    assert not os.path.isfile(script_path), (
        f"sign_message.js already exists at {script_path} — should be created by the agent."
    )


def test_sign_result_not_yet_created():
    result_path = os.path.join(HOME_DIR, "sign_result.json")
    assert not os.path.isfile(result_path), (
        f"sign_result.json already exists at {result_path} — should not exist before the task."
    )
