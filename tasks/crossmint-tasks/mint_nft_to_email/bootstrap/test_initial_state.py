import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"


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


def test_mint_script_not_yet_created():
    script_path = os.path.join(HOME_DIR, "mint_nft.js")
    assert not os.path.isfile(script_path), (
        f"mint_nft.js already exists at {script_path} — it should be created by the agent."
    )


def test_mint_response_not_yet_created():
    result_path = os.path.join(HOME_DIR, "mint_response.json")
    assert not os.path.isfile(result_path), (
        f"mint_response.json already exists at {result_path} — it should not exist before the task."
    )
