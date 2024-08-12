import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.minsubset_checker import minsubset_constants

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = "position_constraints"


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

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=minsubset_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name=f"xml.{RULE_NAME}",
    )

    contains_allowed_position_types_only, issues = _check_allowed_position_types(
        xml_tree=checker_data.input_file_xml_root,
        allowed_position_types=["WorldPosition"],
    )

    if not contains_allowed_position_types_only:
        for issue in issues:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=minsubset_constants.CHECKER_ID,
                description="Issue flagging when input file contains position types other than WorldPosition",
                level=RULE_SEVERITY,
                rule_uid=rule_uid,
            )
            checker_data.result.add_file_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=minsubset_constants.CHECKER_ID,
                issue_id=issue_id,
                row=issue["row"],
                column=issue["column"],
                description=issue["description"],
            )
            checker_data.result.add_xml_location(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=minsubset_constants.CHECKER_ID,
                issue_id=issue_id,
                xpath=str(issue["xpath"]),
                description=issue["description"],
            )
