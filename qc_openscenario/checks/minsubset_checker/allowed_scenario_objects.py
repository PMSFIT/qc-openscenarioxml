import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_allowed_scenario_objects"
CHECKER_DESCRIPTION = "Input file must only contain allowed scenario object types."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.allowed_scenario_objects"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]

ALLOWED_SCENARIO_OBJECTS = [
    "Vehicle",
]


def _contains_allowed_scenario_objects_only(
    xml_tree: etree._ElementTree, allowed_scenario_objects: list[str]
) -> list[dict]:
    """NOTE: Does not handle CatalogReference."""
    issues = []
    xml_scenario_objects = xml_tree.findall(".//ScenarioObject")
    for xml_scenario_object in xml_scenario_objects:
        if not xml_scenario_object[0].tag in allowed_scenario_objects:
            logging.error(
                f"- ScenarioObject not in subset {allowed_scenario_objects}: {xml_scenario_object[0].tag}"
            )
            issues.append(
                {
                    "description": f"ScenarioObject not in subset {allowed_scenario_objects}: {xml_scenario_object[0].tag}",
                    "row": xml_scenario_object.sourceline,
                    "column": 0,
                    "xpath": xml_tree.getpath(xml_scenario_object),
                }
            )
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {RULE_NAME} check")

    issues_allowed_conditions = _contains_allowed_scenario_objects_only(
        xml_tree=checker_data.input_file_xml_root,
        allowed_scenario_objects=ALLOWED_SCENARIO_OBJECTS,
    )

    for issue in issues_allowed_conditions:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains disallowed scenario object",
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
