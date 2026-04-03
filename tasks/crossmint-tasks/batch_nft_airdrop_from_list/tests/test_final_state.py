import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "airdrop.js")
SUMMARY_PATH = os.path.join(HOME_DIR, "airdrop_summary.json")


def test_airdrop_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"airdrop.js not found at {SCRIPT_PATH}."


def test_script_uses_crossmint_api():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "staging.crossmint.com/api/2022-06-09/collections/default/nfts" in content, (
        "airdrop.js must use the Crossmint staging minting API URL."
    )


def test_script_reads_recipients_file():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "recipients.json" in content, (
        "airdrop.js must read from recipients.json."
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
        f"node airdrop.js failed: {result.stderr}"
    )


def test_summary_file_exists():
    assert os.path.isfile(SUMMARY_PATH), f"airdrop_summary.json not found at {SUMMARY_PATH}."


def test_summary_is_valid_json():
    with open(SUMMARY_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"airdrop_summary.json is not valid JSON: {e}")


def test_summary_total_equals_three():
    with open(SUMMARY_PATH) as f:
        data = json.load(f)
    assert "total" in data, "airdrop_summary.json must contain a 'total' field."
    assert data["total"] == 3, (
        f"Expected total=3, got {data.get('total')}."
    )


def test_summary_results_array_length():
    with open(SUMMARY_PATH) as f:
        data = json.load(f)
    assert "results" in data, "airdrop_summary.json must contain a 'results' field."
    assert isinstance(data["results"], list), "results must be an array."
    assert len(data["results"]) == 3, (
        f"Expected 3 results, got {len(data['results'])}."
    )


def test_summary_results_have_email_and_status():
    with open(SUMMARY_PATH) as f:
        data = json.load(f)
    for i, result in enumerate(data["results"]):
        assert "email" in result, f"Result {i} is missing 'email' field."
        assert "status" in result, f"Result {i} is missing 'status' field."
