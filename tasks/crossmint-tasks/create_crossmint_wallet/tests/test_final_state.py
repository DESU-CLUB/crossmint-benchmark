import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
WALLET_RESULT = os.path.join(HOME_DIR, "wallet_result.json")
SCRIPT_PATH = os.path.join(HOME_DIR, "create_wallet.js")


def test_create_wallet_script_exists():
    assert os.path.isfile(SCRIPT_PATH), (
        f"create_wallet.js not found at {SCRIPT_PATH}."
    )


def test_script_uses_crossmint_wallets_sdk():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "@crossmint/wallets-sdk" in content, (
        "create_wallet.js must import from @crossmint/wallets-sdk."
    )
    assert "CrossmintWallets" in content, (
        "create_wallet.js must use CrossmintWallets from @crossmint/wallets-sdk."
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
        f"node create_wallet.js failed with exit code {result.returncode}. stderr: {result.stderr}"
    )


def test_wallet_result_file_exists():
    assert os.path.isfile(WALLET_RESULT), (
        f"wallet_result.json not found at {WALLET_RESULT}."
    )


def test_wallet_result_is_valid_json():
    with open(WALLET_RESULT) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"wallet_result.json is not valid JSON: {e}")


def test_wallet_result_chain_field():
    with open(WALLET_RESULT) as f:
        data = json.load(f)
    assert "chain" in data, "wallet_result.json must contain a 'chain' field."
    assert data["chain"] == "base-sepolia", (
        f"Expected chain 'base-sepolia', got '{data.get('chain')}'."
    )


def test_wallet_result_type_field():
    with open(WALLET_RESULT) as f:
        data = json.load(f)
    assert "type" in data, "wallet_result.json must contain a 'type' field."
    assert data["type"] == "evm-smart-wallet", (
        f"Expected type 'evm-smart-wallet', got '{data.get('type')}'."
    )


def test_wallet_result_has_address_or_error():
    with open(WALLET_RESULT) as f:
        data = json.load(f)
    assert "address" in data or "error" in data, (
        "wallet_result.json must contain either an 'address' field or an 'error' field."
    )
