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
                    "hostname": "mmn.pgcloud.cloud",
                    "port": 5543,
                    "database_type": "postgresql"
                    }
                },
                {
                    "check_type": "database",
                    "details": {
                    "synonym": "MariaDB Database",
                    "hostname": "mariadb.cloud.cloud",
                    "port": 3306,
                    "database_type": "mariadb"
                    }
                },
                {
                    "check_type": "database",
                    "details": {
                    "synonym": "Oracle Database",
                    "hostname": "oracle.cloud.cloud",
                    "port": 1521,
                    "database_type": "oracle"
                    }
                },
                {
                    "check_type": "database",
                    "details": {
                    "synonym": "Microsoft SQL Server",
                    "hostname": "mssql.cloud.cloud",
                    "port": 1433,
                    "database_type": "mssql"
                    }
                },
                {
                    "check_type": "database",
                    "details": {
                    "synonym": "MySQL Database",
                    "hostname": "mysql.cloud.cloud",
                    "port": 3306,
                    "database_type": "mysql"
                    }
                },
                {
                    "check_type": "database",
                    "details": {
                    "synonym": "DB2 Database",
                    "hostname": "db2.cloud.cloud",
                    "port": 50000,
                    "database_type": "db2"
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
def test_successful_database_healthcheck(mock_load_health_check_json_schema,mock_can_establish_tcp):
    # Call /healthcheck/databases with admin default password
    response=client.get("/healthcheck/databases",headers={"Authorization": "Bearer rd-healthcheck"})
    # Make sure that the response is 200
    assert response.status_code==200
    # Load call response
    databases_status=response.json()
    # As healthcheck config contains 6 databases the response should include 6 statuses
    assert len(databases_status)==6
    # Make sure that all responses are databases healthcheck status schema
    databases_healthcheck_status_keys = {'synonym', 'status', 'hostname', 'port', 'can_tcp', 'db_driver_installed'}
    assert all(databases_healthcheck_status_keys.difference(set(item.keys())) ==set() for item in databases_status)

def test_failed_public_access_to_database_healthcheck(mock_load_health_check_json_schema):
    # Call /healthcheck/databases without password
    response=client.get("/healthcheck/databases")
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
def test_failed_wrong_admin_password_to_database_healthcheck(mock_load_health_check_json_schema,admin_password):
    # Call /healthcheck/databases with wrong admin password
    response=client.get("/healthcheck/databases",headers={"Authorization": f"Bearer {admin_password}"})
    # Make sure that the response is 403 Unauthorized
    assert response.status_code==403