import maya.cmds as cmds
from . import joint_utils

def build_ik():
    """
    Main function to build the IK system.
    Selects joints, duplicates them, and sets up the IK hierarchy.

    Requires exactly 3 joints for the rotate plane solver:
    - First joint: base (e.g., shoulder)
    - Second joint: mid (e.g., elbow)
    - Third joint: end (e.g., wrist)

    Returns:
        tuple: (list of created IK joint names, str IK handle name), or (None, None) if invalid selection.
    """
    # Get the currently selected joints
    selected_joints = cmds.ls(selection=True, type='joint')

    # Check if exactly 3 joints are selected
    if not selected_joints:
        cmds.warning("Please select joints to build IK system")
        return None, None
    elif len(selected_joints) != 3:
        cmds.warning("Please select exactly 3 joints for IK setup (e.g., shoulder, elbow, wrist)")
        return None, None

    # Duplicate and rename selected joints, then set up their hierarchy
    ik_joints = joint_utils.duplicate_and_rename_joints(selected_joints, '_IK')

    if ik_joints:
        # Create IK handle
        ik_handle = create_ik_handle(ik_joints[0], ik_joints[-1])
        return ik_joints, ik_handle

    return None, None

def create_ik_handle(start_joint, end_joint):
    """
    Create an IK handle between two joints using rotate plane solver.

    Args:
        start_joint (str): Name of the starting joint (e.g., shoulder)
        end_joint (str): Name of the ending joint (e.g., wrist)

    Returns:
        str: Name of the created IK handle
    """
    # Extract base name from the start joint for naming the IK handle
    base_name = start_joint.replace('_IK', '')
    ik_handle_name = f"{base_name}_ikHandle"

    # Create the IK handle with rotate plane solver
    ik_handle = cmds.ikHandle(
        name=ik_handle_name,
        startJoint=start_joint,
        endEffector=end_joint,
        solver='ikRPsolver',
        sticky='off'
    )

    # The ikHandle command returns a list with [ikHandle, effector]
    # We'll return just the handle name
    return ik_handle[0]

def run():
    """
    Main function to build the IK system.
    This can be called directly from a shelf button.
    """
    return build_ik()

if __name__ == "__main__":
    run()