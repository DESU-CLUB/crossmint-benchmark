import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"
BROKEN_SCRIPT = os.path.join(HOME_DIR, "broken_mint.js")


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist."


def test_node_fetch_installed():
    result = subprocess.run(
        ["node", "-e", "require('node-fetch')"],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
    )
    assert result.returncode == 0, (
        f"node-fetch is not installed: {result.stderr}"
    )


def test_broken_script_exists():
    assert os.path.isfile(BROKEN_SCRIPT), (
        f"broken_mint.js not found at {BROKEN_SCRIPT}. It must be pre-created."
    )


def test_broken_script_has_client_key_bug():
    with open(BROKEN_SCRIPT) as f:
        content = f.read()
    assert "ck_" in content, (
        "broken_mint.js must contain the 'ck_' client key bug."
    )


def test_broken_script_has_pipe_separator_bug():
    with open(BROKEN_SCRIPT) as f:
        content = f.read()
    assert "email|" in content, (
        "broken_mint.js must contain the pipe '|' separator bug in the recipient."
    )


def test_broken_script_has_wrong_url_bug():
    with open(BROKEN_SCRIPT) as f:
        content = f.read()
    # The URL should NOT have staging prefix in the broken version
    assert "https://crossmint.com/api/" in content, (
        "broken_mint.js must use the wrong non-staging URL."
    )


def test_broken_script_missing_image_field():
    with open(BROKEN_SCRIPT) as f:
        content = f.read()
    assert "image" not in content, (
        "broken_mint.js must NOT contain 'image' field (it's missing as a bug)."
    )


def test_fixed_response_not_yet_created():
    result_path = os.path.join(HOME_DIR, "fixed_mint_response.json")
    assert not os.path.isfile(result_path), (
        f"fixed_mint_response.json already exists — should not exist before the task."
    )
