import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_allowed_story_actions"
CHECKER_DESCRIPTION = "Input file must only contain allowed story action types."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.allowed_story_actions"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]


def _check_if_only_one_story_in_storyboard(
    xml_tree: etree._ElementTree,
) -> tuple[bool, list[dict]]:
    status = True
    issues = []
    allowed_number_of_stories = 1
    current_number_of_stories = 0
    xml_storyboards = xml_tree.xpath(".//Storyboard")
    for xml_story in xml_storyboards[0].xpath(".//Story"):
        current_number_of_stories = current_number_of_stories + 1
        if current_number_of_stories > allowed_number_of_stories:
            logging.error(
                f"- More than one story in storyboard ({current_number_of_stories})"
            )
            issue = {
                "description": f"More than one story in storyboard ({current_number_of_stories})",
                "row": xml_story.sourceline,
                "column": 0,
                "xpath": xml_tree.getpath(xml_story),
            }
            status = False
            issues.append(issue)
    return status, issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file complies with the following story constraints:
    * Only allowed to contain one story element
    """
    logging.info(f"Executing {RULE_NAME} check")

    contains_only_one_story, issues = _check_if_only_one_story_in_storyboard(
        xml_tree=checker_data.input_file_xml_root
    )

    if not contains_only_one_story:
        for issue in issues:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=CHECKER_ID,
                description="Issue flagging when input file contains more than one story element",
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
