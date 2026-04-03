import os
import json
import subprocess
import pytest

HOME_DIR = "/home/user"
SERVER_PATH = os.path.join(HOME_DIR, "webhook_server.js")
TEST_PATH = os.path.join(HOME_DIR, "test_webhook.js")
REPORT_PATH = os.path.join(HOME_DIR, "webhook_test_report.json")


def test_webhook_server_exists():
    assert os.path.isfile(SERVER_PATH), f"webhook_server.js not found at {SERVER_PATH}."


def test_test_webhook_exists():
    assert os.path.isfile(TEST_PATH), f"test_webhook.js not found at {TEST_PATH}."


def test_server_uses_express():
    with open(SERVER_PATH) as f:
        content = f.read()
    assert "express" in content, "webhook_server.js must use express."


def test_server_defines_purchase_webhook_route():
    with open(SERVER_PATH) as f:
        content = f.read()
    assert "/webhook/purchase" in content, (
        "webhook_server.js must define POST /webhook/purchase route."
    )


def test_server_defines_health_route():
    with open(SERVER_PATH) as f:
        content = f.read()
    assert "/health" in content, (
        "webhook_server.js must define GET /health route."
    )


def test_server_uses_crossmint_minting_api():
    with open(SERVER_PATH) as f:
        content = f.read()
    assert "staging.crossmint.com/api/2022-06-09/collections/default/nfts" in content, (
        "webhook_server.js must reference the Crossmint staging minting API URL."
    )


def test_server_uses_polygon_amoy_recipient():
    with open(SERVER_PATH) as f:
        content = f.read()
    assert "polygon-amoy" in content, (
        "webhook_server.js must construct recipient with polygon-amoy chain."
    )


def test_server_handles_missing_fields():
    with open(SERVER_PATH) as f:
        content = f.read()
    assert "400" in content or "Missing required" in content, (
        "webhook_server.js must return 400 for missing required fields."
    )


def test_test_script_runs_successfully():
    result = subprocess.run(
        ["node", TEST_PATH],
        capture_output=True,
        text=True,
        cwd=HOME_DIR,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"node test_webhook.js failed: {result.stderr}"
    )


def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"webhook_test_report.json not found at {REPORT_PATH}."


def test_report_is_valid_json():
    with open(REPORT_PATH) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"webhook_test_report.json is not valid JSON: {e}")


def test_report_health_check_true():
    with open(REPORT_PATH) as f:
        data = json.load(f)
    assert "health_check" in data, "webhook_test_report.json must have 'health_check' field."
    assert data["health_check"] is True, (
        f"health_check must be true (server responded to GET /health), got '{data.get('health_check')}'."
    )


def test_report_webhook_response_present():
    with open(REPORT_PATH) as f:
        data = json.load(f)
    assert "webhook_response" in data, (
        "webhook_test_report.json must have 'webhook_response' field."
    )
    assert isinstance(data["webhook_response"], dict), (
        "webhook_response must be a JSON object."
    )
    # Must have status or error field
    resp = data["webhook_response"]
    assert "status" in resp or "error" in resp, (
        "webhook_response must contain 'status' or 'error' field."
    )
