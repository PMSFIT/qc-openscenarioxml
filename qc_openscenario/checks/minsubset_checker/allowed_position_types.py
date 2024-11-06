import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_allowed_position_types"
CHECKER_DESCRIPTION = "Input file must only contain allowed position types."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.allowed_position_types"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]

ALLOWED_POSITION_TYPES = ["WorldPosition"]


def _check_allowed_position_types(
    xml_tree: etree._ElementTree, allowed_position_types: list[str]
) -> tuple[bool, list[dict]]:
    status = True
    issues = []
    for xml_position in xml_tree.iterfind(".//Position"):
        for xml_position_child in xml_position:
            if not xml_position_child.tag in allowed_position_types:
                logging.error(
                    f"- Position not in subset {allowed_position_types}: {xml_position_child.tag}"
                )
                issue = {
                    "description": f"Position not in subset {allowed_position_types}: {xml_position_child.tag}",
                    "row": xml_position_child.sourceline,
                    "column": 0,
                    "xpath": xml_tree.getpath(xml_position_child),
                }
                status = False
                issues.append(issue)
    return status, issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file only contains the following allowed
    position types only:
    * WorldPosition
    """
    logging.info(f"Executing {RULE_NAME} check")

    contains_allowed_position_types_only, issues = _check_allowed_position_types(
        xml_tree=checker_data.input_file_xml_root,
        allowed_position_types=ALLOWED_POSITION_TYPES,
    )

    if not contains_allowed_position_types_only:
        for issue in issues:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description=f"Issue flagging when input file contains position types other than {ALLOWED_POSITION_TYPES}",
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
