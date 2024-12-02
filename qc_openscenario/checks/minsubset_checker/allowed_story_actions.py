import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario import basic_preconditions

CHECKER_ID = "check_asam_xosc_minsubset_allowed_story_actions"
CHECKER_DESCRIPTION = "Input file must only contain allowed story action types."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xosc:1.3.0:minsubset.allowed_story_actions"

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = RULE_UID.split(".")[-1]

ALLOWED_STORYACTIONS = ["RoutingAction", "FollowTrajectoryAction"]
# NOTE: In ALLOWED_STORYACTIONS all the parent types of a specific type have to
# be allowed too (e.g. if FollowTrajectoryAction should be allowed
# RoutingAction has to be allowed).


def _contains_allowed_story_actions_only(
    xml_tree: etree._ElementTree, allowed_actions: list[str]
) -> list[dict]:
    """
    Checks if OpenSCENARIO Story contains allowed action types only.

    Returns list of issues or empty list if no issues occurred.
    """
    issues = []
    for xml_action in xml_tree.iterfind(".//Action"):
        for xml_action_class in xml_action:
            if xml_action_class.tag == "GlobalAction":
                for xml_action_type in xml_action_class:
                    if not xml_action_type in allowed_actions:
                        logging.error(
                            f"- Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}"
                        )
                        issues.append(
                            {
                                "description": f"Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}",
                                "row": xml_action_type.sourceline,
                                "column": 0,
                                "xpath": xml_tree.getpath(xml_action_type),
                            }
                        )
            elif xml_action_class.tag == "UserDefinedAction":
                for xml_action_type in xml_action_class:
                    if not xml_action_type in allowed_actions:
                        logging.error(
                            f"- Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}"
                        )
                        issues.append(
                            {
                                "description": f"Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}",
                                "row": xml_action_type.sourceline,
                                "column": 0,
                                "xpath": xml_tree.getpath(xml_action_type),
                            }
                        )
            elif xml_action_class.tag == "PrivateAction":
                for xml_action_type in xml_action_class:
                    if not xml_action_type.tag in allowed_actions:
                        logging.error(
                            f"- Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}"
                        )
                        issues.append(
                            {
                                "description": f"Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}",
                                "row": xml_action_type.sourceline,
                                "column": 0,
                                "xpath": xml_tree.getpath(xml_action_type),
                            }
                        )
                    else:
                        for xml_action_type_subtype in xml_action_type:
                            if not xml_action_type_subtype.tag in allowed_actions:
                                logging.error(
                                    f"- Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}/{xml_action_type_subtype.tag}"
                                )
                                issues.append(
                                    {
                                        "description": f"Action not in subset {allowed_actions}: {xml_action_class.tag}/{xml_action_type.tag}/{xml_action_type_subtype.tag}",
                                        "row": xml_action_type.sourceline,
                                        "column": 0,
                                        "xpath": xml_tree.getpath(xml_action_type),
                                    }
                                )
    return issues


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Implements a rule to check if input file contains only allowed actions in
    the story.
    """
    logging.info(f"Executing {RULE_NAME} check")

    issues_allowed_story_actions = _contains_allowed_story_actions_only(
        xml_tree=checker_data.input_file_xml_root, allowed_actions=ALLOWED_STORYACTIONS
    )

    for issue in issues_allowed_story_actions:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            description="Issue flagging when input file contains disallowed story actions",
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
