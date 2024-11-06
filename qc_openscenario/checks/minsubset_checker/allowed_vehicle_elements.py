import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_allowed_vehicle_elements"
CHECKER_DESCRIPTION = "Input file must only contain allowed vehicle elements."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.allowed_vehicle_elements"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]

ALLOWED_OPTIONAL_ELEMENTS = []


def _contains_allowed_vehicle_elements_only(
    xml_tree: etree._ElementTree,
) -> list[dict]:
    issues = []
    optional_elements = [
        "ParameterDeclaration",
        "Properties",
        "TrailerHitch",
        "TrailerCoupler",
        "Trailer",
    ]
    xml_vehicles = xml_tree.findall(".//Vehicle")
    for xml_vehicle in xml_vehicles:
        for xml_element in xml_vehicle:
            if (
                xml_element.tag in optional_elements
                and xml_element.tag not in ALLOWED_OPTIONAL_ELEMENTS
            ):
                logging.error(
                    f"- Vehicle contains optional element that is not contained in the subset {ALLOWED_OPTIONAL_ELEMENTS}: {xml_element.tag}"
                )
                issues.append(
                    {
                        "description": f"Vehicle contains optional element that is not contained in the subset {ALLOWED_OPTIONAL_ELEMENTS}: {xml_element.tag}",
                        "row": xml_vehicle.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_vehicle),
                    }
                )
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    logging.info(f"Executing {RULE_NAME} check")

    issues_allowed_vehicle_attrib_and_elements_only = (
        _contains_allowed_vehicle_elements_only(
            xml_tree=checker_data.input_file_xml_root
        )
    )

    for issue in issues_allowed_vehicle_attrib_and_elements_only:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains disallowed vehicle attribute or element",
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
