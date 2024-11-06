import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_openscenario.checks import minsubset_checker


def test_additional_axles_not_allowed_positive(monkeypatch) -> None:
    base_path = "tests/data/minsubset/"
    target_file_name = "minsubset_positive.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            minsubset_checker.additional_axles_not_allowed.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    issues = result.get_issues_by_rule_uid(
        minsubset_checker.additional_axles_not_allowed.RULE_UID
    )
    assert len(issues) == 0

    test_utils.cleanup_files()


def test_additional_axles_not_allowed_negative(monkeypatch) -> None:
    base_path = "tests/data/minsubset/"
    target_file_name = "minsubset_negative.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            minsubset_checker.additional_axles_not_allowed.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    issues = result.get_issues_by_rule_uid(
        minsubset_checker.additional_axles_not_allowed.RULE_UID
    )
    assert len(issues) == 1

    test_utils.cleanup_files()
