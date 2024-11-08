# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pytest
import test_utils
from qc_baselib import Result, IssueSeverity, StatusType
from qc_openscenario.checks import data_type_checker


def test_positive_duration_in_phase_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/positive_duration_in_phase/"
    target_file_name = f"positive_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            data_type_checker.positive_duration_in_phase.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.positive_duration_in_phase"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_positive_duration_in_phase_positive_parameter(
    monkeypatch,
) -> None:
    base_path = "tests/data/positive_duration_in_phase/"
    target_file_name = f"positive_example.parameter.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            data_type_checker.positive_duration_in_phase.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.positive_duration_in_phase"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_positive_duration_in_phase_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/positive_duration_in_phase/"
    target_file_name = f"negative_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            data_type_checker.positive_duration_in_phase.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.positive_duration_in_phase"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_positive_duration_in_phase_negative_parameter(
    monkeypatch,
) -> None:
    base_path = "tests/data/positive_duration_in_phase/"
    target_file_name = f"negative_example.parameter.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            data_type_checker.positive_duration_in_phase.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.positive_duration_in_phase"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_allowed_operators_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"positive_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(data_type_checker.allowed_operators.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.allowed_operators"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_allowed_operators_positive_param(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"positive_example.param.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(data_type_checker.allowed_operators.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.allowed_operators"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_allowed_operators_positive_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"positive_example_multiple.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(data_type_checker.allowed_operators.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.allowed_operators"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_trailer_connect_standard_example(
    monkeypatch,
) -> None:
    base_path = "tests/data/parametric_operator_in_expression/"
    target_file_name = f"TrailerConnect.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(data_type_checker.allowed_operators.CHECKER_ID)
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.allowed_operators"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_allowed_operators_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"negative_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(data_type_checker.allowed_operators.CHECKER_ID)
        == StatusType.COMPLETED
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.allowed_operators"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_allowed_operators_negative_typo(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"negative_example_typo.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(data_type_checker.allowed_operators.CHECKER_ID)
        == StatusType.COMPLETED
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.allowed_operators"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_allowed_operators_negative_multiple(
    monkeypatch,
) -> None:
    base_path = "tests/data/allowed_operators/"
    target_file_name = f"negative_example_multiple.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(data_type_checker.allowed_operators.CHECKER_ID)
        == StatusType.COMPLETED
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.allowed_operators"
    )
    assert len(data_type_issues) == 4
    assert data_type_issues[0].level == IssueSeverity.ERROR
    assert data_type_issues[1].level == IssueSeverity.ERROR
    assert data_type_issues[2].level == IssueSeverity.ERROR
    assert "}" in data_type_issues[0].locations[0].description
    assert "powerer" in data_type_issues[1].locations[0].description
    assert "^" in data_type_issues[2].locations[0].description
    assert "^" in data_type_issues[3].locations[0].description
    test_utils.cleanup_files()


def test_non_negative_transition_time_in_light_state_action_positive(
    monkeypatch,
) -> None:
    base_path = "tests/data/transition_time_should_be_non_negative/"
    target_file_name = f"positive_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            data_type_checker.non_negative_transition_time_in_light_state_action.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    assert (
        len(
            result.get_issues_by_rule_uid(
                "asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action"
            )
        )
        == 0
    )

    test_utils.cleanup_files()


def test_non_negative_transition_time_in_light_state_action_negative(
    monkeypatch,
) -> None:
    base_path = "tests/data/transition_time_should_be_non_negative/"
    target_file_name = f"negative_example.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            data_type_checker.non_negative_transition_time_in_light_state_action.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()


def test_non_negative_transition_time_in_light_state_action_negative_param(
    monkeypatch,
) -> None:
    base_path = "tests/data/transition_time_should_be_non_negative/"
    target_file_name = f"negative_example_param.xosc"
    target_file_path = os.path.join(base_path, target_file_name)

    test_utils.create_test_config(target_file_path)

    test_utils.launch_main(monkeypatch)

    result = Result()
    result.load_from_file(test_utils.REPORT_FILE_PATH)

    assert (
        result.get_checker_status(
            data_type_checker.non_negative_transition_time_in_light_state_action.CHECKER_ID
        )
        == StatusType.COMPLETED
    )

    data_type_issues = result.get_issues_by_rule_uid(
        "asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action"
    )
    assert len(data_type_issues) == 1
    assert data_type_issues[0].level == IssueSeverity.ERROR
    test_utils.cleanup_files()
