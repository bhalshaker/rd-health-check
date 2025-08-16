import os
import pytest

from app.controller.healthcheck_foundation import HealthCheckFoundation


def test_is_config_template_checktype_valid_with_all_types_returns_true():
    config = [
        {
            "check_type": "mount_point",
            "details": {
                "synonym": "root",
                "mount_point": "/",
                "threshold_percentage": 80,
            },
        },
        {
            "check_type": "webservice",
            "details": {
                "synonym": "api",
                "hostname": "localhost",
                "port": 8080,
                "protocol": "http",
            },
        },
        {
            "check_type": "database",
            "details": {
                "synonym": "db",
                "hostname": "localhost",
                "port": 5432,
                "database_type": "postgresql",
            },
        },
        {
            "check_type": "requirements",
            "details": {
                "synonym": "reqs",
                "requirements_file_path": "requirements.txt",
            },
        },
    ]
    assert HealthCheckFoundation.is_config_template_checktype_valid(config) is True

@pytest.mark.parametrize(
    "check_type",
    [
        ("mount_point"),
        ("MOUNT_POINT"),
        ("webservice"),
        ("weBseRvice"),
        ("database"),
        ("dataBASE"),
        ("requirements"),
        ("rEqUiRemEnTs")
    ]
)
def test_is_valid_health_check_type_accepts_allowed_values_case_insensitive(check_type):
    assert HealthCheckFoundation.is_valid_health_check_type(check_type) is True

@pytest.mark.parametrize(
    "check_type",
    [
        ("mountpoint"),
        ("WEB_SERVICE"),
        ("CAMOMILE")
    ]
)
def test_invalid_health_check_types(check_type):
    assert HealthCheckFoundation.is_valid_health_check_type(check_type) is False

@pytest.mark.parametrize(
    "mount_point",
    [
        ({ "synonym": "root","mount_point": "/","threshold_percentage": 70}),
        ({ "synonym": "attachment","mount_point": "/att_doc","threshold_percentage": 90}),
        ({ "synonym": "app data","mount_point": "/app","threshold_percentage": 80})
    ]
)
def test_mount_point_template_verification_with_required_keys_returns_true(mount_point):
    assert HealthCheckFoundation.mount_point_template_vertification(mount_point) is True


def test_is_config_template_checktype_valid_returns_false_for_empty_list():
    assert HealthCheckFoundation.is_config_template_checktype_valid([]) is False


def test_requirements_template_verification_accepts_dict_with_expected_keys():
    requirements = {
        "synonym": "reqs",
        "requirements_file_path": "requirements.txt",
    }
    assert HealthCheckFoundation.requirements_template_verification(requirements) is True



def test_is_config_template_checktype_valid_fails_when_list_contains_non_dict():
    valid_mount = {
        "check_type": "mount_point",
        "details": {
            "synonym": "root",
            "mount_point": "/",
            "threshold_percentage": 80,
        },
    }
    config = [valid_mount, "not a dict"]
    assert HealthCheckFoundation.is_config_template_checktype_valid(config) is False


def test_webservice_template_verification_with_required_keys_returns_true():
    webservice = {
        "synonym": "api",
        "hostname": "localhost",
        "port": 8080,
        "protocol": "http",
    }
    assert HealthCheckFoundation.webservice_template_verification(webservice) is True


def test_webservice_template_verification_accepts_list_of_keys():
    # Even though this is not a dict, 'in' checks membership of strings in list and passes
    keys_list = ["synonym", "hostname", "port", "protocol"]
    assert HealthCheckFoundation.webservice_template_verification(keys_list) is True