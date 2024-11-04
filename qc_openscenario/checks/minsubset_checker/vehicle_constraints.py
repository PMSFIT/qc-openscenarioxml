import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.minsubset_checker import minsubset_constants


RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = "vehicle_constraints"

ALLOWED_SCENARIO_OBJECTS = [
    "Vehicle",
]
ALLOWED_OPTIONAL_ATTRIBUTES = []
ALLOWED_OPTIONAL_ELEMENTS = []
ALLOWED_OPTIONAL_PERFORMANCE_ATTRIBUTES = []
ADDITIONAL_AXLES_ALLOWED = False


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


def _contains_allowed_vehicle_attributes_and_elements_only(
    xml_tree: etree._ElementTree,
) -> list[dict]:
    issues = []
    optional_attributes = ["mass", "model3d", "role"]
    optional_elements = [
        "ParameterDeclaration",
        "Properties",
        "TrailerHitch",
        "TrailerCoupler",
        "Trailer",
    ]
    xml_vehicles = xml_tree.findall(".//Vehicle")
    for xml_vehicle in xml_vehicles:
        for attr in optional_attributes:
            if attr in xml_vehicle.attrib and attr not in ALLOWED_OPTIONAL_ATTRIBUTES:
                logging.error(
                    f"- Vehicle contains optional attribute that is not contained in the subset {ALLOWED_OPTIONAL_ATTRIBUTES}: {attr}"
                )
                issues.append(
                    {
                        "description": f"Vehicle contains optional attribute that is not contained in the subset {ALLOWED_OPTIONAL_ATTRIBUTES}: {attr}",
                        "row": xml_vehicle.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_vehicle),
                    }
                )
        for xml_element in xml_vehicle:
            if (
                xml_element.tag in optional_elements
                and xml_element.tag not in ALLOWED_OPTIONAL_PERFORMANCE_ATTRIBUTES
            ):
                logging.error(
                    f"- Vehicle contains optional element that is not contained in the subset {ALLOWED_OPTIONAL_PERFORMANCE_ATTRIBUTES}: {xml_element.tag}"
                )
                issues.append(
                    {
                        "description": f"Vehicle contains optional element that is not contained in the subset {ALLOWED_OPTIONAL_PERFORMANCE_ATTRIBUTES}: {xml_element.tag}",
                        "row": xml_vehicle.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_vehicle),
                    }
                )
    return issues


def _contains_allowed_performance_attributes_only(
    xml_tree: etree._ElementTree,
) -> list[dict]:
    issues = []
    optional_attributes = ["maxAccelerationRate", "maxDecelerationRate"]
    for xml_performance in xml_tree.findall(".//Performance"):
        for attr in xml_performance.attrib:
            if attr in optional_attributes:
                logging.error(
                    f"- Performance contains optional attribute that is not contained in minimal subset {ALLOWED_OPTIONAL_ELEMENTS}: {attr}"
                )
                issues.append(
                    {
                        "description": f"Vehicle contains optional attribute that is not contained in minimal subset {ALLOWED_OPTIONAL_ELEMENTS}: {attr}",
                        "row": xml_performance.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_performance),
                    }
                )
    return issues


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


def _vehicle_contains_additional_axles(xml_tree: etree._ElementTree) -> list[dict]:
    issues = []
    for xml_axles in xml_tree.findall(".//Axles"):
        if xml_axles.xpath(f".//AdditionalAxle"):
            logging.error(
                f"- Vehicle contains AdditionalAxle that is not allowed in the subset"
            )
            issues.append(
                {
                    "description": f"Vehicle contains AdditionalAxle that is not allowed in the subset",
                    "row": xml_axles.sourceline,
                    "column": 0,
                    "xpath": xml_tree.getpath(xml_axles),
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

    issues_allowed_scenario_objects = _contains_allowed_scenario_objects_only(
        xml_tree=checker_data.input_file_xml_root,
        allowed_scenario_objects=ALLOWED_SCENARIO_OBJECTS,
    )

    for issue in issues_allowed_scenario_objects:
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

    issues_allowed_vehicle_attrib_and_elements_only = (
        _contains_allowed_vehicle_attributes_and_elements_only(
            xml_tree=checker_data.input_file_xml_root
        )
    )

    for issue in issues_allowed_vehicle_attrib_and_elements_only:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains disallowed vehicle attribute or element",
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

    issues_allowed_performance_attributes_only = (
        _contains_allowed_performance_attributes_only(
            xml_tree=checker_data.input_file_xml_root
        )
    )

    for issue in issues_allowed_performance_attributes_only:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains disallowed performance attribute",
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

    issues_vehicle_lacks_front_axle = _vehicle_lacks_front_axle(
        xml_tree=checker_data.input_file_xml_root
    )

    for issue in issues_vehicle_lacks_front_axle:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains vehicle without FrontAxle",
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

    if not ADDITIONAL_AXLES_ALLOWED:
        issue_contains_additional_axles = _vehicle_contains_additional_axles(
            xml_tree=checker_data.input_file_xml_root
        )

        for issue in issue_contains_additional_axles:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=minsubset_constants.CHECKER_ID,
                description="Issue flagging when input file contains AdditionalAxle",
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
