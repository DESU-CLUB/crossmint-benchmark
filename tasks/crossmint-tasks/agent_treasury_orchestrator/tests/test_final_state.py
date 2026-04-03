import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
TREASURY_PATH = os.path.join(HOME_DIR, "treasury.js")
HARNESS_PATH = os.path.join(HOME_DIR, "run_treasury_tests.js")
RESULTS_PATH = os.path.join(HOME_DIR, "treasury_test_results.json")


def test_treasury_module_exists():
    assert os.path.isfile(TREASURY_PATH), f"treasury.js not found at {TREASURY_PATH}."


def test_treasury_uses_crossmint_wallets_sdk():
    with open(TREASURY_PATH) as f:
        content = f.read()
    assert "@crossmint/wallets-sdk" in content, (
        "treasury.js must import from @crossmint/wallets-sdk."
    )


def test_treasury_exports_execute_function():
    with open(TREASURY_PATH) as f:
        content = f.read()
    assert "executeTreasuryAction" in content, (
        "treasury.js must define and export executeTreasuryAction."
    )
    assert "module.exports" in content, (
        "treasury.js must use module.exports to export the function."
    )


def test_treasury_uses_crossmint_minting_api():
    with open(TREASURY_PATH) as f:
        content = f.read()
    assert "staging.crossmint.com" in content, (
        "treasury.js must reference staging.crossmint.com for API calls."
    )


def test_test_harness_exists():
    assert os.path.isfile(HARNESS_PATH), f"run_treasury_tests.js not found at {HARNESS_PATH}."


def test_harness_runs_successfully():
    result = subprocess.run(
        ["node", HARNESS_PATH],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"node run_treasury_tests.js failed: {result.stderr}"
    )


def test_results_file_exists():
    assert os.path.isfile(RESULTS_PATH), f"treasury_test_results.json not found at {RESULTS_PATH}."


def test_results_is_valid_json():
    with open(RESULTS_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"treasury_test_results.json is not valid JSON: {e}")


def test_results_is_array_of_three():
    with open(RESULTS_PATH) as f:
        data = json.load(f)
    assert isinstance(data, list), "treasury_test_results.json must be a JSON array."
    assert len(data) == 3, (
        f"Expected 3 results (one per action type), got {len(data)}."
    )


def test_results_have_required_fields():
    with open(RESULTS_PATH) as f:
        data = json.load(f)
    for i, item in enumerate(data):
        assert "action_type" in item, f"Result {i} is missing 'action_type' field."
        assert "result" in item, f"Result {i} is missing 'result' field."


def test_results_cover_all_action_types():
    with open(RESULTS_PATH) as f:
        data = json.load(f)
    action_types = {item["action_type"] for item in data}
    expected = {"create_wallet", "check_balance", "mint_receipt"}
    assert expected == action_types, (
        f"Expected action types {expected}, got {action_types}."
    )
