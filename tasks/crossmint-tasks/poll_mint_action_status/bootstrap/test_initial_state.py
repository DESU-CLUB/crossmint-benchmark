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


def test_mint_and_poll_script_not_yet_created():
    script_path = os.path.join(HOME_DIR, "mint_and_poll.js")
    assert not os.path.isfile(script_path), (
        f"mint_and_poll.js already exists — should be created by the agent."
    )


def test_poll_result_not_yet_created():
    result_path = os.path.join(HOME_DIR, "poll_result.json")
    assert not os.path.isfile(result_path), (
        f"poll_result.json already exists — should not exist before the task."
    )
