import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_allowed_init_actions"
CHECKER_DESCRIPTION = "Input file must only contain allowed init action types."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.allowed_init_actions"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]

ALLOWED_INITACTIONS = ["TeleportAction"]


def _contains_allowed_init_actions_only(
    xml_tree: etree._ElementTree, allowed_actions: list[str]
) -> list[dict]:
    """
    Checks if OpenSCENARIO Init contains allowed action types only.

    Returns list of issues or empty list if no issues occurred.
    """
    issues = []
    for xml_actions in xml_tree.iterfind(".//Actions"):
        for xml_action in xml_actions:
            if xml_action.tag == "GlobalAction":
                for xml_global_action_type in xml_action:
                    if not xml_global_action_type in allowed_actions:
                        logging.error(
                            f"- Action not in subset {allowed_actions}: {xml_action.tag}/{xml_global_action_type.tag}"
                        )
                        issues.append(
                            {
                                "description": f"Action not in subset {allowed_actions}: {xml_action.tag}/{xml_global_action_type.tag}",
                                "row": xml_global_action_type.sourceline,
                                "column": 0,
                                "xpath": xml_tree.getpath(xml_global_action_type),
                            }
                        )
            elif xml_action.tag == "Private":
                for xml_private_action in xml_action:
                    for xml_private_action_type in xml_private_action:
                        if not xml_private_action_type.tag in allowed_actions:
                            logging.error(
                                f"- Action not in subset {allowed_actions}: {xml_private_action.tag}/{xml_private_action_type.tag}"
                            )
                            issues.append(
                                {
                                    "description": f"Action not in subset {allowed_actions}: {xml_private_action.tag}/{xml_private_action_type.tag}",
                                    "row": xml_private_action_type.sourceline,
                                    "column": 0,
                                    "xpath": xml_tree.getpath(xml_private_action_type),
                                }
                            )
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file complies with following action constraints:

    Allowed Actions in Init:
    * TeleportAction

    Allowed Action in Story:
    * RoutingAction
        * FollowTrajectoryAction
            * Constraints:
                * allowed_shapes=["Polyline"],
                * allowed_following_modes=["position"],
                * allowed_timing_domains=["absolute"],
                * timing_offset_allowed=False,
                * timing_scale_allowed=False
    """
    logging.info(f"Executing {RULE_NAME} check")

    issues_allowed_init_actions = _contains_allowed_init_actions_only(
        xml_tree=checker_data.input_file_xml_root, allowed_actions=ALLOWED_INITACTIONS
    )

    for issue in issues_allowed_init_actions:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains disallowed init actions",
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
