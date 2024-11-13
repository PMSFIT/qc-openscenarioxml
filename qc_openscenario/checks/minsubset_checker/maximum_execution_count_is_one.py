import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_maximum_execution_count_is_one"
CHECKER_DESCRIPTION = "Input file must contain a maximum of one action (and correspondingly one event and maneuver) per maneuver group."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.maximum_execution_count_is_one"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]


def _check_maximum_execution_count(
    xml_tree: etree._ElementTree,
) -> list[dict]:
    issues = []
    for xml_maneuver_group in xml_tree.findall(".//ManeuverGroup"):
        max_execution_count = int(xml_maneuver_group.attrib["maximumExecutionCount"])
        if max_execution_count != 1:
            logging.error(
                f"- Maximum execution count of ManeuverGroup is not one (maximumExecutionCount: {max_execution_count})"
            )
            issue = {
                "description": f"Maximum execution count of ManeuverGroup is not one (maximumExecutionCount: {max_execution_count})",
                "row": xml_maneuver_group.sourceline,
                "column": 0,
                "xpath": xml_tree.getpath(xml_maneuver_group),
            }
            issues.append(issue)
    for xml_event in xml_tree.findall(".//Event"):
        if "maximumExecutionCount" in xml_event.attrib:
            max_execution_count = int(xml_event.attrib["maximumExecutionCount"])
        else:
            max_execution_count = (
                1  # OpenSCENARIO does not specify what happens when not defined
            )
        if max_execution_count != 1:
            logging.error(
                f"- Maximum execution count of Event is not one (maximumExecutionCount: {max_execution_count})"
            )
            issue = {
                "description": f"Maximum execution count of Event is not one (maximumExecutionCount: {max_execution_count})",
                "row": xml_event.sourceline,
                "column": 0,
                "xpath": xml_tree.getpath(xml_event),
            }
            issues.append(issue)
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {RULE_NAME} check")

    issues = _check_maximum_execution_count(xml_tree=checker_data.input_file_xml_root)

    for issue in issues:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when maneuver group or event has maximum execution count > 1",
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
