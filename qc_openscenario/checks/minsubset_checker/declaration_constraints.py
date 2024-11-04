import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.minsubset_checker import minsubset_constants

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = "declaration_constraints"


def _no_variables(xml_tree: etree._ElementTree) -> list[dict]:
    """
    Checks if OpenSCENARIO file contains no variable declarations and
    accordingly no variables.

    Returns list of issues or empty list if no issues occurred.
    """
    issues = []
    xml_variable_declarations = xml_tree.findall(".//VariableDeclaration")
    for xml_variable_declaration in xml_variable_declarations:
        variable_name = xml_variable_declaration.get("name")
        logging.error(f"- Found VariableDeclaration: {variable_name}")
        issue = {
            "description": f"Found VariableDeclaration: {variable_name}",
            "row": xml_variable_declaration.sourceline,
            "column": 0,
            "xpath": xml_tree.getpath(xml_variable_declaration),
        }
        issues.append(issue)
    return issues


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


def _no_monitors(xml_tree: etree._ElementTree) -> list[dict]:
    """
    Checks if OpenSCENARIO file contains no monitor declarations and
    accordingly no monitors.

    Returns list of issues or empty list if no issues occurred.
    """
    issues = []
    xml_monitor_declarations = xml_tree.findall(".//MonitorDeclaration")
    for xml_monitor_declaration in xml_monitor_declarations:
        monitor_name = xml_monitor_declaration.get("name")
        logging.error(f"- Found MonitorDeclaration: {monitor_name}")
        issue = {
            "description": f"Found MonitorDeclaration: {monitor_name}",
            "row": xml_monitor_declaration.sourceline,
            "column": 0,
            "xpath": xml_tree.getpath(xml_monitor_declaration),
        }
        issues.append(issue)
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file complies with following paramter constraints:
    * No use of variables
    * No use of parameters
    * No use of monitors
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

    issues_variables = _no_variables(xml_tree=checker_data.input_file_xml_root)

    for issue in issues_variables:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains variables",
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

    issues_parameters = _no_parameters(xml_tree=checker_data.input_file_xml_root)

    for issue in issues_parameters:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains parameters",
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

    issues_monitors = _no_monitors(xml_tree=checker_data.input_file_xml_root)

    for issue in issues_monitors:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains monitors",
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
