import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist."


def test_crossmint_wallets_sdk_installed():
    result = subprocess.run(
        ["node", "-e", "require('@crossmint/wallets-sdk')"],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
    )
    assert result.returncode == 0, (
        f"@crossmint/wallets-sdk is not installed: {result.stderr}"
    )


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


def test_treasury_module_not_yet_created():
    script_path = os.path.join(HOME_DIR, "treasury.js")
    assert not os.path.isfile(script_path), (
        f"treasury.js already exists — should be created by the agent."
    )


def test_test_harness_not_yet_created():
    harness_path = os.path.join(HOME_DIR, "run_treasury_tests.js")
    assert not os.path.isfile(harness_path), (
        f"run_treasury_tests.js already exists — should be created by the agent."
    )


def test_treasury_results_not_yet_created():
    results_path = os.path.join(HOME_DIR, "treasury_test_results.json")
    assert not os.path.isfile(results_path), (
        f"treasury_test_results.json already exists — should not exist before the task."
    )
