import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_max_one_action_per_act"
CHECKER_DESCRIPTION = "Input file must contain a maximum of one action (and correspondingly one event and maneuver) per act."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.max_one_action_per_act"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]


def _max_one_action_per_act(
    xml_tree: etree._ElementTree,
) -> list[dict]:
    issues = []
    for xml_act in xml_tree.findall(".//Act"):
        xml_actions_in_act = xml_act.findall(".//Action")
        if len(xml_actions_in_act) > 1:
            logging.error(
                f"- Found more than one action in act ({len(xml_actions_in_act)})"
            )
            issue = {
                "description": f"Found more than one action in act ({len(xml_actions_in_act)})",
                "row": xml_act.sourceline,
                "column": 0,
                "xpath": xml_tree.getpath(xml_act),
            }
            issues.append(issue)
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {RULE_NAME} check")

    issues = _max_one_action_per_act(xml_tree=checker_data.input_file_xml_root)

    for issue in issues:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains more than one action per act",
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
