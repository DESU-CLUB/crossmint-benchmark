import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "sign_message.js")
RESULT_PATH = os.path.join(HOME_DIR, "sign_result.json")


def test_sign_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"sign_message.js not found at {SCRIPT_PATH}."


def test_script_uses_crossmint_wallets_sdk():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "@crossmint/wallets-sdk" in content, (
        "sign_message.js must import from @crossmint/wallets-sdk."
    )
    assert "createCrossmint" in content, (
        "sign_message.js must use createCrossmint from @crossmint/wallets-sdk."
    )
    assert "CrossmintWallets" in content, (
        "sign_message.js must use CrossmintWallets from @crossmint/wallets-sdk."
    )


def test_script_runs_successfully():
    result = subprocess.run(
        ["node", SCRIPT_PATH],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"node sign_message.js failed: {result.stderr}"
    )


def test_sign_result_exists():
    assert os.path.isfile(RESULT_PATH), f"sign_result.json not found at {RESULT_PATH}."


def test_sign_result_is_valid_json():
    with open(RESULT_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"sign_result.json is not valid JSON: {e}")


def test_sign_result_chain_field():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert data.get("chain") == "base-sepolia", (
        f"Expected chain 'base-sepolia', got '{data.get('chain')}'."
    )


def test_sign_result_message_field():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert data.get("message") == "Hello from Crossmint", (
        f"Expected message 'Hello from Crossmint', got '{data.get('message')}'."
    )


def test_sign_result_wallet_type_field():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert data.get("wallet_type") == "evm-smart-wallet", (
        f"Expected wallet_type 'evm-smart-wallet', got '{data.get('wallet_type')}'."
    )


def test_sign_result_has_signature_or_error():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert "signature" in data or "error" in data, (
        "sign_result.json must contain either a 'signature' or an 'error' field."
    )
