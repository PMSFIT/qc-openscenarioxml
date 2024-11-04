import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.minsubset_checker import minsubset_constants

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = "catalog_constraints"


def _check_catalog_references(xml_tree: etree._ElementTree) -> tuple[bool, list[dict]]:
    status = True
    issues = []
    xml_catalog_refs = xml_tree.xpath(".//CatalogReference")

    for xml_catalog_ref in xml_catalog_refs:
        logging.error(f"- CatalogReference used")
        issue = {
            "description": f"CatalogReference used",
            "row": xml_catalog_ref.sourceline,
            "column": 0,
            "xpath": xml_tree.getpath(xml_catalog_ref),
        }
        status = False
        issues.append(issue)
    return status, issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file complies with the following catalog reference constraints:
    * Only allowed to contain one story element
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

    contains_only_one_story, issues = _check_catalog_references(
        xml_tree=checker_data.input_file_xml_root
    )

    if not contains_only_one_story:
        for issue in issues:
            issue_id = checker_data.result.register_issue(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=minsubset_constants.CHECKER_ID,
                description="Issue flagging when input file does not comply with catalog constraints",
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
