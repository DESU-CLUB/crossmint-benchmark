import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "broken_mint.js")
RESPONSE_PATH = os.path.join(HOME_DIR, "fixed_mint_response.json")


def test_fixed_script_no_client_key_prefix():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "ck_" not in content, (
        "broken_mint.js must not contain 'ck_' client-side key prefix after fix."
    )


def test_fixed_script_no_pipe_separator():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "email|" not in content, (
        "broken_mint.js must not use pipe separator 'email|' after fix."
    )


def test_fixed_script_correct_recipient_format():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "email:test@example.com:polygon-amoy" in content, (
        "broken_mint.js must use correct colon-separated recipient 'email:test@example.com:polygon-amoy'."
    )


def test_fixed_script_correct_url():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "staging.crossmint.com/api/" in content, (
        "broken_mint.js must use staging.crossmint.com URL after fix."
    )


def test_fixed_script_has_image_field():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "image" in content, (
        "broken_mint.js must contain 'image' in metadata after fix."
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
        f"node broken_mint.js failed after fix: {result.stderr}"
    )


def test_fixed_response_exists():
    assert os.path.isfile(RESPONSE_PATH), (
        f"fixed_mint_response.json not found at {RESPONSE_PATH}."
    )


def test_fixed_response_is_valid_json():
    with open(RESPONSE_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"fixed_mint_response.json is not valid JSON: {e}")
