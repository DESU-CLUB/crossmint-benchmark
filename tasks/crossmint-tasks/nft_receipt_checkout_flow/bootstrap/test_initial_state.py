import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist."


def test_express_installed():
    result = subprocess.run(
        ["node", "-e", "require('express')"],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
    )
    assert result.returncode == 0, (
        f"express is not installed: {result.stderr}"
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


def test_webhook_server_not_yet_created():
    script_path = os.path.join(HOME_DIR, "webhook_server.js")
    assert not os.path.isfile(script_path), (
        f"webhook_server.js already exists — should be created by the agent."
    )


def test_test_webhook_not_yet_created():
    test_path = os.path.join(HOME_DIR, "test_webhook.js")
    assert not os.path.isfile(test_path), (
        f"test_webhook.js already exists — should be created by the agent."
    )


def test_webhook_report_not_yet_created():
    report_path = os.path.join(HOME_DIR, "webhook_test_report.json")
    assert not os.path.isfile(report_path), (
        f"webhook_test_report.json already exists — should not exist before the task."
    )
