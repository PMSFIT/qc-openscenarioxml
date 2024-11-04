import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.minsubset_checker import minsubset_constants

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = "entities_constraints"

ALLOWED_SCENARIO_OBJECTS = [
    "Vehicle",
]
ENTITY_SELECTION_ALLOWED = False
OBJECT_CONTROLLER_ALLOWED = False


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

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=minsubset_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name=f"xml.{RULE_NAME}",
    )

    issues_allowed_conditions = _contains_allowed_scenario_objects_only(
        xml_tree=checker_data.input_file_xml_root,
        allowed_scenario_objects=ALLOWED_SCENARIO_OBJECTS,
    )

    for issue in issues_allowed_conditions:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains disallowed scenario object",
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
