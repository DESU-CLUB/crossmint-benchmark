import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "mint_nft.js")
RESPONSE_PATH = os.path.join(HOME_DIR, "mint_response.json")


def test_mint_script_exists():
    assert os.path.isfile(SCRIPT_PATH), (
        f"mint_nft.js not found at {SCRIPT_PATH}."
    )


def test_script_uses_crossmint_staging_api():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "staging.crossmint.com/api/2022-06-09/collections/default/nfts" in content, (
        "mint_nft.js must use the Crossmint staging minting API URL."
    )


def test_script_sets_recipient():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "email:test@example.com:polygon-amoy" in content, (
        "mint_nft.js must set recipient to 'email:test@example.com:polygon-amoy'."
    )


def test_script_sets_nft_name():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "Welcome NFT" in content, (
        "mint_nft.js must include NFT name 'Welcome NFT' in metadata."
    )


def test_script_sets_api_key_header():
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "x-api-key" in content, (
        "mint_nft.js must set the x-api-key header."
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
        f"node mint_nft.js failed with exit code {result.returncode}. stderr: {result.stderr}"
    )


def test_mint_response_file_exists():
    assert os.path.isfile(RESPONSE_PATH), (
        f"mint_response.json not found at {RESPONSE_PATH}."
    )


def test_mint_response_is_valid_json():
    with open(RESPONSE_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"mint_response.json is not valid JSON: {e}")


def test_mint_response_written_by_script():
    # The file must be parseable as a JSON object (dict), not just any value
    with open(RESPONSE_PATH) as f:
        data = json.load(f)
    assert isinstance(data, dict), (
        f"mint_response.json must be a JSON object, got: {type(data)}"
    )
