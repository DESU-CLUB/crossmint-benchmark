import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"
BROKEN_SCRIPT = os.path.join(HOME_DIR, "broken_wallet.js")


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


def test_broken_script_exists():
    assert os.path.isfile(BROKEN_SCRIPT), (
        f"broken_wallet.js not found at {BROKEN_SCRIPT}. It must be pre-created."
    )


def test_broken_script_has_wrong_chain():
    with open(BROKEN_SCRIPT) as f:
        content = f.read()
    assert "base_sepolia" in content, (
        "broken_wallet.js must contain the 'base_sepolia' chain name bug (underscore)."
    )


def test_broken_script_has_email_recovery_bug():
    with open(BROKEN_SCRIPT) as f:
        content = f.read()
    assert "'email'" in content or '"email"' in content, (
        "broken_wallet.js must contain the wrong email recovery type bug."
    )


def test_wallet_debug_result_not_yet_created():
    result_path = os.path.join(HOME_DIR, "wallet_debug_result.json")
    assert not os.path.isfile(result_path), (
        f"wallet_debug_result.json already exists — should not exist before the task."
    )


def test_debug_notes_not_yet_created():
    notes_path = os.path.join(HOME_DIR, "debug_notes.txt")
    assert not os.path.isfile(notes_path), (
        f"debug_notes.txt already exists — should be created by the agent."
    )
