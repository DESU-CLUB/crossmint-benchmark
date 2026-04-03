import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "broken_wallet.js")
RESULT_PATH = os.path.join(HOME_DIR, "wallet_debug_result.json")
NOTES_PATH = os.path.join(HOME_DIR, "debug_notes.txt")


def test_fixed_script_no_underscore_chain():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "base_sepolia" not in content, (
        "broken_wallet.js must not use 'base_sepolia' (underscore) after fix."
    )


def test_fixed_script_uses_correct_chain():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "base-sepolia" in content, (
        "broken_wallet.js must use 'base-sepolia' (hyphen) after fix."
    )


def test_fixed_script_uses_server_recovery():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "server" in content, (
        "broken_wallet.js must use server recovery type after fix."
    )


def test_fixed_script_runs_successfully():
    result = subprocess.run(
        ["node", SCRIPT_PATH],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"node broken_wallet.js failed after fix: {result.stderr}"
    )


def test_wallet_debug_result_exists():
    assert os.path.isfile(RESULT_PATH), (
        f"wallet_debug_result.json not found at {RESULT_PATH}."
    )


def test_wallet_debug_result_is_valid_json():
    with open(RESULT_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"wallet_debug_result.json is not valid JSON: {e}")


def test_wallet_debug_result_chain():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert data.get("chain") == "base-sepolia", (
        f"Expected chain 'base-sepolia' in wallet_debug_result.json, got '{data.get('chain')}'."
    )


def test_debug_notes_exist():
    assert os.path.isfile(NOTES_PATH), (
        f"debug_notes.txt not found at {NOTES_PATH}."
    )


def test_debug_notes_contain_bug_and_fix():
    with open(NOTES_PATH) as f:
        content = f.read()
    assert "BUG:" in content, (
        "debug_notes.txt must contain at least one 'BUG:' line."
    )
    assert "FIX:" in content, (
        "debug_notes.txt must contain at least one 'FIX:' line."
    )
