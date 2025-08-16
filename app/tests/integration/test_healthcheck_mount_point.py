import pytest
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

@pytest.fixture
def mock_load_health_check_json_schema(monkeypatch):
    def get_config_dict(config_file_location):
        return [
                    {
                        "check_type": "mount_point",
                        "details": {
                        "synonym": "Attachments Partition",
                        "mount_point": "/boot",
                        "threshold_percentage": 45
                        }
                    },
                    {
                        "check_type": "mount_point",
                        "details": {
                        "synonym": "Root Partition",
                        "mount_point": "/",
                        "threshold_percentage": 85
                        }
                    }
                ]

    monkeypatch.setattr("app.controller.external_file_processing.ExternalFileProcessing.load_health_check_json_schema",
                        get_config_dict)

@pytest.fixture
def mock_mount_point(monkeypatch):
    def is_mounted(mount_point):
        return True
    monkeypatch.setattr("app.controller.healthcheck_foundation.HealthCheckFoundation.is_file_system_mounted",
                        is_mounted)

@pytest.fixture
def mock_mount_point_usage(monkeypatch):
    def mount_point_usage(mount_point):
        return 45
    monkeypatch.setattr("app.controller.terminal_processing.TerminalProcessing.get_mount_point_usages",
                        mount_point_usage)

def test_successful_mount_points_healthcheck(mock_load_health_check_json_schema,mock_mount_point,mock_mount_point_usage):
    # Call /healthcheck/mountpoints with admin default password
    response=client.get("/healthcheck/mountpoints",headers={"Authorization": "Bearer rd-healthcheck"})
    # Make sure that the response is 200
    assert response.status_code==200
    # Load call response
    mount_points_status=response.json()
    print(mount_points_status)
    # As healthcheck config contains 2 mount_points the response should include 2 statuses
    assert len(mount_points_status)==2
    # Make sure that all responses are mount points healthcheck status schema
    webservice_healthcheck_status_keys={'synonym', 'status', 'mount_point', 'is_mounted', 'current_usage', 'threshold_percentage'}
    assert all(webservice_healthcheck_status_keys.difference(set(item.keys())) ==set() for item in mount_points_status)

def test_failed_public_access_to_mountpoints_healthcheck(mock_load_health_check_json_schema):
    # Call /healthcheck/mountpoints without password
    response=client.get("/healthcheck/mountpoints")
    # Make sure that the response is 403 Unauthorized
    assert response.status_code==403

@pytest.mark.parametrize(
    "admin_password",
    [
        ("Rd-healthcheck"),
        ("rdhealthcheck"),
        ("wrong_password")
    ]
)
def test_failed_wrong_admin_password_to_mountpoints_healthcheck(mock_load_health_check_json_schema,admin_password):
    # Call /healthcheck/mountpoints with wrong admin password
    response=client.get("/healthcheck/mountpoints",headers={"Authorization": f"Bearer {admin_password}"})
    # Make sure that the response is 403 Unauthorized
    assert response.status_code==403