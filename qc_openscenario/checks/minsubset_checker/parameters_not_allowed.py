import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_parameters_not_allowed"
CHECKER_DESCRIPTION = "Input file must not contain parameter declarations."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.parameters_not_allowed"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]


def _no_parameters(xml_tree: etree._ElementTree) -> list[dict]:
    """
    Checks if OpenSCENARIO file contains no parameter declarations and
    accordingly no parameters.

    Returns list of issues or empty list if no issues occurred.
    """
    issues = []
    xml_parameter_declarations = xml_tree.findall(".//ParameterDeclaration")
    for xml_parameter_declaration in xml_parameter_declarations:
        param_name = xml_parameter_declaration.get("name")
        logging.error(f"- Found ParameterDeclaration: {param_name}")
        issue = {
            "description": f"Found ParameterDeclaration: {param_name}",
            "row": xml_parameter_declaration.sourceline,
            "column": 0,
            "xpath": xml_tree.getpath(xml_parameter_declaration),
        }
        issues.append(issue)
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file complies with following constraints:
    * No use of parameters
    """
    logging.info(f"Executing {RULE_NAME} check")

    issues_parameters = _no_parameters(xml_tree=checker_data.input_file_xml_root)

    for issue in issues_parameters:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains parameters",
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
