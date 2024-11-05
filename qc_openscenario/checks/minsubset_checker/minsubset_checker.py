import logging

from qc_baselib import StatusType

from qc_openscenario import constants
from qc_openscenario.checks import models

from qc_openscenario import basic_preconditions

from qc_openscenario.checks.minsubset_checker import (
    action_constraints,
    catalog_constraints,
    condition_constraints,
    declaration_constraints,
    enitities_constraints,
    minsubset_constants,
    position_constraints,
    story_constraints,
    vehicle_constraints,
)

CHECKER_ID = "minsubset_xosc"
CHECKER_DESCRIPTION = "Minimal OpenSCENARIO subset based on polyline trajectories"
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset"


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info("Executing minsubset checks")

    rule_list = [
        action_constraints.check_rule,
        catalog_constraints.check_rule,
        declaration_constraints.check_rule,
        enitities_constraints.check_rule,
        position_constraints.check_rule,
        condition_constraints.check_rule,
        story_constraints.check_rule,
        vehicle_constraints.check_rule,
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
