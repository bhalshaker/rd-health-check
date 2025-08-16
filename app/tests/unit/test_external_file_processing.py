import pytest
import json
from pathlib import Path
from app.controller.external_file_processing import ExternalFileProcessing

@pytest.fixture
def tmp_requirements_file(tmp_path):
    content = """\
    # This is a comment
    packageA==1.0.0
    packageB[extra]==2.0.0
    package_c
    """
    req_file = tmp_path / "requirements.txt"
    req_file.write_text(content)
    return req_file

@pytest.fixture
def tmp_empty_requirements_file(tmp_path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("")
    return req_file

@pytest.fixture
def tmp_health_check_file(tmp_path):
    data = [
        {"name": "check1", "status": "ok"},
        {"name": "check2", "status": "fail"},
    ]
    hc_file = tmp_path / "health_check_schema.json"
    hc_file.write_text(json.dumps(data))
    return hc_file

@pytest.fixture
def tmp_invalid_health_check_file(tmp_path):
    hc_file = tmp_path / "health_check_schema.json"
    hc_file.write_text(json.dumps({"not": "a list"}))
    return hc_file

def test_read_packages_requirements_reads_packages(tmp_requirements_file, monkeypatch):
    monkeypatch.setattr(ExternalFileProcessing, "file_exists", lambda f: True)
    packages = ExternalFileProcessing.read_packages_requirements(str(tmp_requirements_file))
    assert packages == ["packageA", "packageB", "package_c"]

def test_read_packages_requirements_returns_empty_on_missing_file(monkeypatch):
    monkeypatch.setattr(ExternalFileProcessing, "file_exists", lambda f: False)
    packages = ExternalFileProcessing.read_packages_requirements("missing.txt")
    assert packages == []

def test_read_packages_requirements_returns_empty_on_empty_file(tmp_empty_requirements_file, monkeypatch):
    monkeypatch.setattr(ExternalFileProcessing, "file_exists", lambda f: True)
    packages = ExternalFileProcessing.read_packages_requirements(str(tmp_empty_requirements_file))
    assert packages == []

def test_load_health_check_json_schema_returns_list(tmp_health_check_file, monkeypatch):
    monkeypatch.setattr(ExternalFileProcessing, "file_exists", lambda f: True)
    schema = ExternalFileProcessing.load_health_check_json_schema(str(tmp_health_check_file))
    assert isinstance(schema, list)
    assert schema[0]["name"] == "check1"

def test_load_health_check_json_schema_returns_empty_on_nonlist(tmp_invalid_health_check_file, monkeypatch):
    monkeypatch.setattr(ExternalFileProcessing, "file_exists", lambda f: True)
    schema = ExternalFileProcessing.load_health_check_json_schema(str(tmp_invalid_health_check_file))
    assert schema == []

def test_load_health_check_json_schema_returns_empty_on_missing_file(monkeypatch):
    monkeypatch.setattr(ExternalFileProcessing, "file_exists", lambda f: False)
    schema = ExternalFileProcessing.load_health_check_json_schema("missing.json")
    assert schema == []

def test_file_exists_true(tmp_requirements_file):
    assert ExternalFileProcessing.file_exists(str(tmp_requirements_file))

def test_file_exists_false(tmp_path):
    missing_file = tmp_path / "does_not_exist.txt"
    assert not ExternalFileProcessing.file_exists(str(missing_file))