import pytest
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

@pytest.fixture
def mock_load_health_check_json_schema(monkeypatch):
    def get_config_dict(config_file_location):
        return [
                {
                    "check_type": "database",
                    "details": {
                    "synonym": "Core Database",
                    "hostname": "mozilla.cloudflare-dns.com",
                    "port": 443,
                    "database_type": "mysql"
                    }
                },
                {
                    "check_type": "webservice",
                    "details": {
                    "synonym": "example API",
                    "hostname": "example.com",
                    "port": 443,
                    "protocol": "https"
                    }
                },
                {
                    "check_type": "mount_point",
                    "details": {
                    "synonym": "Attachments Partition",
                    "mount_point": "/boot",
                    "threshold_percentage": 45
                    }
                },
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
def mock_can_establish_tcp(monkeypatch):
    def can_establish_tcp_mock(hostname,port,timeout=0):
        return True
    monkeypatch.setattr("app.controller.tcp_based_connection.TcpBasedConnection.establish_tcp_connection",
                        can_establish_tcp_mock)

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
@pytest.fixture
def mock_load_requirements_file(monkeypatch):
    def load_requirements_file(config_file_location):
        return ['uvicorn','zeep','pyjwt','fastapi','django','flask']

    monkeypatch.setattr("app.controller.external_file_processing.ExternalFileProcessing.read_packages_requirements",
                        load_requirements_file)
    
def test_successful_webservice_healthcheck(mock_load_health_check_json_schema,
                                           mock_can_establish_tcp,
                                           mock_mount_point,
                                           mock_mount_point_usage,
                                           mock_load_requirements_file):
    # Call /healthcheck
    response=client.get("/healthcheck")
    # Make sure that the response is 200
    assert response.status_code==200
    # Load call response
    all_status=response.json()
    # by default response schema has the following fields {'mount_points','webservices','databases','requirements_files'}
    assert set(all_status.keys()).difference({'mount_points','webservices','databases','requirements_files'})==set()
    # assume each status type has one element in it is list assmuing checkconfig dictionary is correct
    assert all(len(all_status.get(item))==1 for item in all_status)