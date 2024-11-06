import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_allowed_vehicle_performance_attributes"
CHECKER_DESCRIPTION = (
    "Input file must only contain allowed vehicle performance attributes."
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.allowed_vehicle_performance_attributes"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]

ALLOWED_OPTIONAL_PERFORMANCE_ATTRIBUTES = []


def _contains_allowed_performance_attributes_only(
    xml_tree: etree._ElementTree,
) -> list[dict]:
    issues = []
    optional_attributes = ["maxAccelerationRate", "maxDecelerationRate"]
    for xml_performance in xml_tree.findall(".//Performance"):
        for attr in xml_performance.attrib:
            if attr in optional_attributes:
                logging.error(
                    f"- Performance contains optional attribute that is not contained in minimal subset {ALLOWED_OPTIONAL_PERFORMANCE_ATTRIBUTES}: {attr}"
                )
                issues.append(
                    {
                        "description": f"Vehicle contains optional attribute that is not contained in minimal subset {ALLOWED_OPTIONAL_PERFORMANCE_ATTRIBUTES}: {attr}",
                        "row": xml_performance.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_performance),
                    }
                )
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {RULE_NAME} check")

    issues_allowed_performance_attributes_only = (
        _contains_allowed_performance_attributes_only(
            xml_tree=checker_data.input_file_xml_root
        )
    )

    for issue in issues_allowed_performance_attributes_only:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains disallowed performance attribute",
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
