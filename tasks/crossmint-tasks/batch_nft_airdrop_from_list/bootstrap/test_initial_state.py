import os
import shutil
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
RECIPIENTS_FILE = os.path.join(HOME_DIR, "recipients.json")


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist."


def test_recipients_file_exists():
    assert os.path.isfile(RECIPIENTS_FILE), (
        f"recipients.json not found at {RECIPIENTS_FILE}. It must be pre-populated."
    )


def test_recipients_file_is_valid_json():
    with open(RECIPIENTS_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"recipients.json is not valid JSON: {e}")


def test_recipients_file_has_three_entries():
    with open(RECIPIENTS_FILE) as f:
        data = json.load(f)
    assert isinstance(data, list), "recipients.json must be a JSON array."
    assert len(data) == 3, (
        f"recipients.json must contain 3 email addresses, got {len(data)}."
    )


def test_recipients_contains_expected_emails():
    with open(RECIPIENTS_FILE) as f:
        data = json.load(f)
    expected = {"alice@example.com", "bob@example.com", "carol@example.com"}
    assert set(data) == expected, (
        f"recipients.json must contain alice, bob, carol. Got: {data}"
    )


def test_airdrop_script_not_yet_created():
    script_path = os.path.join(HOME_DIR, "airdrop.js")
    assert not os.path.isfile(script_path), (
        f"airdrop.js already exists — it should be created by the agent."
    )


def test_airdrop_summary_not_yet_created():
    summary_path = os.path.join(HOME_DIR, "airdrop_summary.json")
    assert not os.path.isfile(summary_path), (
        f"airdrop_summary.json already exists — it should not exist before the task."
    )
