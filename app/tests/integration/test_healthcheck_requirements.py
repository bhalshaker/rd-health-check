import pytest
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

@pytest.fixture
def mock_load_health_check_json_schema(monkeypatch):
    def get_config_dict(config_file_location):
        return [
                {
                    "check_type":"requirements",
                    "details":{
                        "synonym":"Requirements Files",
                        "requirements_file_path":"requirements.txt"
                    }
                }
                ]

    monkeypatch.setattr("app.controller.external_file_processing.ExternalFileProcessing.load_health_check_json_schema",
                        get_config_dict)

@pytest.fixture
def mock_load_requirements_file(monkeypatch):
    def load_requirements_file(config_file_location):
        return ['uvicorn','zeep','pyjwt','fastapi','django','flask']

    monkeypatch.setattr("app.controller.external_file_processing.ExternalFileProcessing.read_packages_requirements",
                        load_requirements_file)

def test_successful_requirements_healthcheck(mock_load_health_check_json_schema,mock_load_requirements_file):
    # Call /healthcheck/requirements with admin default password
    response=client.get("/healthcheck/requirements",headers={"Authorization": "Bearer rd-healthcheck"})
    # Make sure that the response is 200
    assert response.status_code==200
    # Load call response
    requirements_status=response.json()
    # As healthcheck config contains 1 requirements check the response should include 1 statuse
    assert len(requirements_status)==1
    # Make sure that all responses are requirements healthcheck status schema
    requirements_healthcheck_status_keys={'synonym', 'status', 'requirements_file_path', 'is_file_exists', 'are_all_packages_installed'}
    assert all(requirements_healthcheck_status_keys.difference(set(item.keys())) ==set() for item in requirements_status)

def test_failed_public_access_to_requirements_healthcheck(mock_load_health_check_json_schema):
    # Call /healthcheck/requirements without password
    response=client.get("/healthcheck/requirements")
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
def test_failed_wrong_admin_password_to_requirement_healthcheck(mock_load_health_check_json_schema,admin_password):
    # Call /healthcheck/requirements with wrong admin password
    response=client.get("/healthcheck/requirements",headers={"Authorization": f"Bearer {admin_password}"})
    # Make sure that the response is 403 Unauthorized
    assert response.status_code==403