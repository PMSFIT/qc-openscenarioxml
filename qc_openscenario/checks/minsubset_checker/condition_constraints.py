import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.minsubset_checker import minsubset_constants

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = "condition_constraints"


def _contains_allowed_conditions_only(
    xml_tree: etree._ElementTree, allowed_conditions: list[str]
) -> list[dict]:
    issues = []
    for xml_condition in xml_tree.iterfind(".//Condition"):
        for xml_condition_type in xml_condition:
            if not xml_condition_type.tag in allowed_conditions:
                logging.error(
                    f"- Condition not in subset {str(allowed_conditions)}: {xml_condition_type.tag}"
                )
                issues.append(
                    {
                        "description": f"Condition not in subset {str(allowed_conditions)}: {xml_condition_type.tag}",
                        "row": xml_condition_type.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_condition_type),
                    }
                )
            else:
                for xml_condition_type_subtype in xml_condition_type:
                    if not xml_condition_type_subtype.tag in allowed_conditions:
                        logging.error(
                            f"- Condition not in subset {str(allowed_conditions)}: {xml_condition_type.tag}/{xml_condition_type_subtype.tag}"
                        )
                        issues.append(
                            {
                                "description": f"Condition not in subset {str(allowed_conditions)}: {xml_condition_type.tag}/{xml_condition_type_subtype.tag}",
                                "row": xml_condition_type.sourceline,
                                "column": 0,
                                "xpath": xml_tree.getpath(xml_condition_type),
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

    issues_allowed_conditions = _contains_allowed_conditions_only(
        xml_tree=checker_data.input_file_xml_root,
        allowed_conditions=[
            "ByValueCondition",
            "SimulationTimeCondition",
            "StoryboardElementStateCondition",
        ],
    )

    for issue in issues_allowed_conditions:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains disallowed trigger conditions",
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
