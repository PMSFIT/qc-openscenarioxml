import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_stop_triggers_not_allowed_except_in_storyboard"
CHECKER_DESCRIPTION = "Input file must not contain any stop triggers except a stop trigger in the storyboard."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = (
    "asam.net:xosc:1.3.0:minsubset.stop_triggers_not_allowed_except_in_storyboard"
)

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]


def _no_triggers_except_storyboard_stop_trigger(
    xml_tree: etree._ElementTree,
) -> list[dict]:
    issues = []
    for xml_stop_trigger in xml_tree.findall(".//StopTrigger"):
        if xml_stop_trigger.getparent().tag != "Storyboard":
            logging.error(f"- Found disallowed StopTrigger")
            issue = {
                "description": f"Found disallowed StopTrigger",
                "row": xml_stop_trigger.sourceline,
                "column": 0,
                "xpath": xml_tree.getpath(xml_stop_trigger),
            }
            issues.append(issue)
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {RULE_NAME} check")

    issues_vehicle_lacks_front_axle = _no_triggers_except_storyboard_stop_trigger(
        xml_tree=checker_data.input_file_xml_root
    )

    for issue in issues_vehicle_lacks_front_axle:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains disallowed StopTrigger",
            level=RULE_SEVERITY,
            rule_uid=RULE_UID,
        )
        checker_data.result.add_file_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            row=issue["row"],
            column=issue["column"],
            description=issue["description"],
        )
        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            xpath=str(issue["xpath"]),
            description=issue["description"],
        )
