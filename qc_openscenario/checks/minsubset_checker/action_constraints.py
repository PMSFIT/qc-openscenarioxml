import logging

from lxml import etree

from qc_baselib import Configuration, Result, IssueSeverity

from qc_openscenario import constants
from qc_openscenario.checks import utils, models

from qc_openscenario.checks.minsubset_checker import minsubset_constants

RULE_SEVERITY = IssueSeverity.INFORMATION
RULE_NAME = "action_constraints"

ALLOWED_INITACTIONS = ["TeleportAction"]
ALLOWED_STORYACTIONS = ["RoutingAction", "FollowTrajectoryAction"]
FOLLOWTRAJECTORYACTION_CONSTRAINTS = {
    "allowed_shapes": ["Polyline"],
    "allowed_following_modes": ["position"],
    "allowed_timing_domains": ["absolute"],
    "timing_offset_allowed": False,
    "timing_scale_allowed": False,
}


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


def _check_FollowTrajectoryAction_constraints(
    xml_tree: etree._ElementTree,
    allowed_shapes: list[str],
    allowed_following_modes: list[str],
    allowed_timing_domains: list[str],
    timing_offset_allowed: bool,
    timing_scale_allowed: bool,
) -> list[dict]:
    """
    Checks if all FollowTrajectoryAction elements comply with the given constraints
    (allowed trajectory shapes, allowed trajectory following modes, etc.).

    Returns list of issues or empty list if no issues occurred.
    """
    issues = []
    for xml_follow_trajectory_action in xml_tree.iterfind(".//FollowTrajectoryAction"):
        xml_trajectoryref = xml_follow_trajectory_action.find("TrajectoryRef")
        xml_trajectory = xml_trajectoryref.find("Trajectory")
        if xml_trajectory != None:
            xml_shape = xml_trajectory.find("Shape")
            for xml_shape_child in xml_shape:
                if not xml_shape_child.tag in allowed_shapes:
                    logging.error(
                        f"- Trajectory shape not in subset {str(allowed_shapes)}: {xml_shape_child.tag}"
                    )
                    issues.append(
                        {
                            "description": f"Trajectory shape not in subset {str(allowed_shapes)}: {xml_shape_child.tag}",
                            "row": xml_shape_child.sourceline,
                            "column": 0,
                            "xpath": xml_tree.getpath(xml_shape_child),
                        }
                    )
        xml_following_mode = xml_follow_trajectory_action.find(
            "TrajectoryFollowingMode"
        )
        if xml_following_mode != None:
            following_mode = xml_following_mode.attrib["followingMode"]
            if not following_mode in allowed_following_modes:
                logging.error(
                    f"- Following mode not in subset {str(allowed_following_modes)}: {following_mode}"
                )
                issues.append(
                    {
                        "description": f"Trajectory following mode not in subset {str(allowed_following_modes)}: {following_mode}",
                        "row": xml_following_mode.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_following_mode),
                    }
                )
        xml_time_reference = xml_follow_trajectory_action.find("TimeReference")
        for xml_time_reference_child in xml_time_reference:
            if xml_time_reference_child.tag == "None":
                logging.error(f"- Trajectory time reference is None")
                issues.append(
                    {
                        "description": f"Trajectory time reference is None",
                        "row": xml_time_reference_child.sourceline,
                        "column": 0,
                        "xpath": xml_tree.getpath(xml_time_reference_child),
                    }
                )
            elif xml_time_reference_child.tag == "Timing":
                domain_absolute_relative = xml_time_reference_child.attrib[
                    "domainAbsoluteRelative"
                ]
                offset = xml_time_reference_child.attrib["offset"]
                scale = xml_time_reference_child.attrib["scale"]
                if (
                    domain_absolute_relative not in allowed_timing_domains
                    or (timing_offset_allowed or offset == 0)
                    or (timing_scale_allowed or scale == 1)
                ):
                    logging.error(
                        f"- Trajectory timing constraints not met (allowed timing domains: {allowed_timing_domains}, offset allowed: {timing_offset_allowed}, scale allowed: {timing_scale_allowed})"
                    )
                    issues.append(
                        {
                            "description": f"Trajectory timing constraints not met (allowed timing domains: {allowed_timing_domains}, offset allowed: {timing_offset_allowed}, scale allowed: {timing_scale_allowed})",
                            "row": xml_time_reference_child.sourceline,
                            "column": 0,
                            "xpath": xml_tree.getpath(xml_time_reference_child),
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

    rule_uid = checker_data.result.register_rule(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=minsubset_constants.CHECKER_ID,
        emanating_entity="asam.net",
        standard="xosc",
        definition_setting="1.0.0",
        rule_full_name=f"xml.{RULE_NAME}",
    )

    issues_allowed_init_actions = _contains_allowed_init_actions_only(
        xml_tree=checker_data.input_file_xml_root, allowed_actions=ALLOWED_INITACTIONS
    )

    for issue in issues_allowed_init_actions:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains disallowed init actions",
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

    issues_allowed_story_actions = _contains_allowed_story_actions_only(
        xml_tree=checker_data.input_file_xml_root,
        allowed_actions=ALLOWED_STORYACTIONS,
    )

    for issue in issues_allowed_story_actions:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file contains disallowed story actions",
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

    issues_FollowTrajectoryAction_constraints = (
        _check_FollowTrajectoryAction_constraints(
            xml_tree=checker_data.input_file_xml_root,
            allowed_shapes=FOLLOWTRAJECTORYACTION_CONSTRAINTS["allowed_shapes"],
            allowed_following_modes=FOLLOWTRAJECTORYACTION_CONSTRAINTS[
                "allowed_following_modes"
            ],
            allowed_timing_domains=FOLLOWTRAJECTORYACTION_CONSTRAINTS[
                "allowed_timing_domains"
            ],
            timing_offset_allowed=FOLLOWTRAJECTORYACTION_CONSTRAINTS[
                "timing_offset_allowed"
            ],
            timing_scale_allowed=FOLLOWTRAJECTORYACTION_CONSTRAINTS[
                "timing_scale_allowed"
            ],
        )
    )

    for issue in issues_FollowTrajectoryAction_constraints:
        issue_id = checker_data.result.register_issue(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            description="Issue flagging when input file does not comply with FollowTrajectoryAction constraints",
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
        # NOTE: Adding another location does not extend existing 'Locations' tag but creates another 'Locations' tag
        checker_data.result.add_xml_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=minsubset_constants.CHECKER_ID,
            issue_id=issue_id,
            xpath=str(issue["xpath"]),
            description=issue["description"],
        )
