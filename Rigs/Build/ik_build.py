import maya.cmds as cmds
from . import joint_utils

def build_ik():
    """
    Main function to build the IK system.
    Selects joints and duplicates them with IK suffix.

    Returns:
        list: List of created IK joint names, or None if no joints were selected.
    """
    # Get the currently selected joints
    selected_joints = cmds.ls(selection=True, type='joint')

    # Check if any joints are selected
    if not selected_joints:
        cmds.warning("Please select joints to build IK system")
        return None

    # Duplicate and rename selected joints
    ik_joints = joint_utils.duplicate_and_rename_joints(selected_joints, '_IK')

    return ik_joints

def run():
    """
    Main function to build the IK system.
    This can be called directly from a shelf button.
    """
    return build_ik()

if __name__ == "__main__":
    run()