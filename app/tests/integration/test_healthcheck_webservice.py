import pytest
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

@pytest.fixture
def mock_load_health_check_json_schema(monkeypatch):
    def get_config_dict(config_file_location):
        return [
            {
                "check_type": "webservice",
                "details": {
                    "synonym": "First API",
                    "hostname": "google.com",
                    "port": 443,
                    "protocol": "https"
                    }
                },
                {
                    "check_type": "webservice",
                    "details": {
                    "synonym": "Second API",
                    "hostname": "bing.com",
                    "port": 443,
                    "protocol": "https"
                    }
                },
                {
                    "check_type": "webservice",
                    "details": {
                    "synonym": "Third API",
                    "hostname": "yahoo.com",
                    "port": 443,
                    "protocol": "https"
                    }
                },
                {
                    "check_type": "webservice",
                    "details": {
                    "synonym": "Fourth API",
                    "hostname": "duckduckgo.com",
                    "port": 443,
                    "protocol": "https"
                    }
                }
                ]

    monkeypatch.setattr("app.controller.external_file_processing.ExternalFileProcessing.load_health_check_json_schema",
                        get_config_dict)

def test_successful_webservice_healthcheck(mock_load_health_check_json_schema):
    # Call /healthcheck/webservices with admin default password
    response=client.get("/healthcheck/webservices",headers={"Authorization": "Bearer rd-healthcheck"})
    # Make sure that the response is 200
    assert response.status_code==200
    # Load call response
    webservices_status=response.json()
    # As healthcheck config contains 4 webservices the response should include 4 statuses
    assert len(webservices_status)==4
    # Make sure that all responses are webservice healthcheck status schema
    webservice_healthcheck_status_keys={'synonym', 'status', 'hostname', 'port', 'protocol', 'can_tcp'}
    assert all(set(item.keys())== (webservice_healthcheck_status_keys) for item in webservices_status)

def test_failed_public_access_to_webservice_healthcheck(mock_load_health_check_json_schema):
    # Call /healthcheck/webservices without password
    response=client.get("/healthcheck/webservices")
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
def test_failed_wrong_admin_password_to_webservice_healthcheck(mock_load_health_check_json_schema,admin_password):
    # Call /healthcheck/webservices with wrong admin password
    response=client.get("/healthcheck/webservices",headers={"Authorization": f"Bearer {admin_password}"})
    # Make sure that the response is 403 Unauthorized
    assert response.status_code==403