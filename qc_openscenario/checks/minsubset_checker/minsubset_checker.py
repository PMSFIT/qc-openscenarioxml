import logging

from qc_baselib import Configuration, Result, StatusType

from qc_openscenario import constants
from qc_openscenario.checks import utils, models
from qc_openscenario.schema import schema_files

from qc_openscenario.checks.minsubset_checker import (
    action_constraints,
    condition_constraints,
    minsubset_constants,
    position_constraints,
)


def run_checks(checker_data: models.CheckerData) -> None:
    logging.info("Executing minsubset checks")

    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=minsubset_constants.CHECKER_ID,
        description="Check if input file complies with minimal xosc subset",
        summary="",
    )

    if checker_data.input_file_xml_root is None:
        logging.error(
            f"Invalid xml input file. Checker {minsubset_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    if checker_data.result.get_checker_issue_count("xoscBundle", "schema_xosc") > 0:
        logging.error(
            f"Invalid xosc input file. Checker {minsubset_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    if checker_data.result.get_checker_issue_count("xoscBundle", "reference_xosc") > 0:
        logging.error(
            f"Invalid reference(s) in input file. Checker {minsubset_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    if checker_data.result.get_checker_issue_count("xoscBundle", "data_type_xosc") > 0:
        logging.error(
            f"Invalid data_type properties in input file. Checker {minsubset_constants.CHECKER_ID} skipped"
        )
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            status=StatusType.SKIPPED,
        )
        return

    rule_list = [
        action_constraints.check_rule,
        position_constraints.check_rule,
        condition_constraints.check_rule,
    ]

    for rule in rule_list:
        rule(checker_data=checker_data)

    logging.info(
        f"Issues found - {checker_data.result.get_checker_issue_count(checker_bundle_name=constants.BUNDLE_NAME, checker_id=minsubset_constants.CHECKER_ID)}"
    )

    checker_data.result.set_checker_status(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=minsubset_constants.CHECKER_ID,
        status=StatusType.COMPLETED,
    )
