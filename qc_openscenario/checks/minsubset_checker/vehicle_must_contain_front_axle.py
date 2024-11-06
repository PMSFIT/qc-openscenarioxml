import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_vehicle_must_contain_front_axle"
CHECKER_DESCRIPTION = "Input file must only contain vehicles with front axle."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.vehicle_must_contain_front_axle"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]


def _vehicle_lacks_front_axle(xml_tree: etree._ElementTree) -> list[dict]:
    issues = []
    for xml_axles in xml_tree.findall(".//Axles"):
        if not xml_axles.xpath(f".//FrontAxle"):
            logging.error(f"- Vehicle does not contain a FrontAxle")
            issues.append(
                {
                    "description": f"Vehicle does not contain a FrontAxle",
                    "row": xml_axles.sourceline,
                    "column": 0,
                    "xpath": xml_tree.getpath(xml_axles),
                }
            )
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {RULE_NAME} check")

    issues_vehicle_lacks_front_axle = _vehicle_lacks_front_axle(
        xml_tree=checker_data.input_file_xml_root
    )

    for issue in issues_vehicle_lacks_front_axle:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains vehicle without FrontAxle",
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
