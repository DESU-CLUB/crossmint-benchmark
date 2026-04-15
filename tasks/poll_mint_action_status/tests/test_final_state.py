import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "mint_and_poll.js")
RESULT_PATH = os.path.join(HOME_DIR, "poll_result.json")


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"mint_and_poll.js not found at {SCRIPT_PATH}."


def test_script_uses_crossmint_minting_api():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "staging.crossmint.com/api/2022-06-09/collections/default/nfts" in content, (
        "mint_and_poll.js must POST to the Crossmint minting API endpoint."
    )


def test_script_uses_action_status_api():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "actions" in content, (
        "mint_and_poll.js must GET the Crossmint action status endpoint (containing 'actions')."
    )


def test_script_implements_polling():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "actionId" in content, (
        "mint_and_poll.js must extract and use actionId from the mint response."
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
        f"node mint_and_poll.js failed: {result.stderr}"
    )


def test_poll_result_exists():
    assert os.path.isfile(RESULT_PATH), f"poll_result.json not found at {RESULT_PATH}."


def test_poll_result_is_valid_json():
    with open(RESULT_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"poll_result.json is not valid JSON: {e}")


def test_poll_result_action_id_field():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert "actionId" in data, "poll_result.json must contain an 'actionId' field."


def test_poll_result_final_status_field():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert "final_status" in data, "poll_result.json must contain a 'final_status' field."


def test_poll_result_poll_attempts_field():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert "poll_attempts" in data, "poll_result.json must contain a 'poll_attempts' field."
    attempts = data["poll_attempts"]
    assert isinstance(attempts, int), f"poll_attempts must be an integer, got {type(attempts)}."
    assert 0 <= attempts <= 5, f"poll_attempts must be between 0 and 5, got {attempts}."


def test_poll_result_mint_chain_field():
    with open(RESULT_PATH) as f:
        data = json.load(f)
    assert data.get("mint_chain") == "polygon-amoy", (
        f"Expected mint_chain 'polygon-amoy', got '{data.get('mint_chain')}'."
    )
