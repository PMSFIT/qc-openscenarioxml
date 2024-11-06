import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_monitors_not_allowed"
CHECKER_DESCRIPTION = "Input file must not contain monitor declarations."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.monitors_not_allowed"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]


def _no_monitors(xml_tree: etree._ElementTree) -> list[dict]:
    """
    Checks if OpenSCENARIO file contains no monitor declarations and
    accordingly no monitors.

    Returns list of issues or empty list if no issues occurred.
    """
    issues = []
    xml_monitor_declarations = xml_tree.findall(".//MonitorDeclaration")
    for xml_monitor_declaration in xml_monitor_declarations:
        monitor_name = xml_monitor_declaration.get("name")
        logging.error(f"- Found MonitorDeclaration: {monitor_name}")
        issue = {
            "description": f"Found MonitorDeclaration: {monitor_name}",
            "row": xml_monitor_declaration.sourceline,
            "column": 0,
            "xpath": xml_tree.getpath(xml_monitor_declaration),
        }
        issues.append(issue)
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file complies with following constraints:
    * No use of monitors
    """
    logging.info(f"Executing {RULE_NAME} check")

    issues_monitors = _no_monitors(xml_tree=checker_data.input_file_xml_root)

    for issue in issues_monitors:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains monitors",
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