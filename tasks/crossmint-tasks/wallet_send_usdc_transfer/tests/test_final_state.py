import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "transfer_usdc.js")
LOG_PATH = os.path.join(HOME_DIR, "transfer_log.json")
USDC_CONTRACT = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"


def test_transfer_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"transfer_usdc.js not found at {SCRIPT_PATH}."


def test_script_uses_crossmint_wallets_sdk():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "@crossmint/wallets-sdk" in content, (
        "transfer_usdc.js must import from @crossmint/wallets-sdk."
    )
    assert "CrossmintWallets" in content, (
        "transfer_usdc.js must use CrossmintWallets."
    )
    assert "createCrossmint" in content, (
        "transfer_usdc.js must use createCrossmint."
    )


def test_script_references_usdc_contract():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert USDC_CONTRACT in content, (
        f"transfer_usdc.js must reference the USDC contract address {USDC_CONTRACT}."
    )


def test_script_runs_successfully():
    result = subprocess.run(
        ["node", SCRIPT_PATH],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"node transfer_usdc.js failed: {result.stderr}"
    )


def test_transfer_log_exists():
    assert os.path.isfile(LOG_PATH), f"transfer_log.json not found at {LOG_PATH}."


def test_transfer_log_is_valid_json():
    with open(LOG_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"transfer_log.json is not valid JSON: {e}")


def test_transfer_log_sender_chain():
    with open(LOG_PATH) as f:
        data = json.load(f)
    assert data.get("sender_chain") == "base-sepolia", (
        f"Expected sender_chain 'base-sepolia', got '{data.get('sender_chain')}'."
    )


def test_transfer_log_receiver_chain():
    with open(LOG_PATH) as f:
        data = json.load(f)
    assert data.get("receiver_chain") == "base-sepolia", (
        f"Expected receiver_chain 'base-sepolia', got '{data.get('receiver_chain')}'."
    )


def test_transfer_log_amount():
    with open(LOG_PATH) as f:
        data = json.load(f)
    assert data.get("amount") == "0.001", (
        f"Expected amount '0.001', got '{data.get('amount')}'."
    )


def test_transfer_log_token():
    with open(LOG_PATH) as f:
        data = json.load(f)
    assert data.get("token") == "USDC", (
        f"Expected token 'USDC', got '{data.get('token')}'."
    )


def test_transfer_log_addresses():
    with open(LOG_PATH) as f:
        data = json.load(f)
    assert "sender_address" in data, "transfer_log.json must have 'sender_address'."
    assert "receiver_address" in data, "transfer_log.json must have 'receiver_address'."


def test_transfer_log_status():
    with open(LOG_PATH) as f:
        data = json.load(f)
    assert "transfer_status" in data, "transfer_log.json must have 'transfer_status'."
    valid_statuses = {"submitted", "failed", "mock"}
    assert data["transfer_status"] in valid_statuses, (
        f"transfer_status must be one of {valid_statuses}, got '{data['transfer_status']}'."
    )
