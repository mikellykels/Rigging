import maya.cmds as cmds
from . import joint_utils

def build_fk():
    """
    Main function to build the FK system.
    Selects joints, duplicates them, and sets up the FK hierarchy.

    Returns:
        list: List of created FK joint names, or None if no joints were selected.
    """
    # Get the currently selected joints
    selected_joints = cmds.ls(selection=True, type='joint')

    # Check if any joints are selected
    if not selected_joints:
        cmds.warning("Please select joints to build FK system")
        return None

    # Duplicate and rename selected joints
    fk_joints = joint_utils.duplicate_and_rename_joints(selected_joints, '_FK')

    return fk_joints

def run():
    """
    Main function to build the FK system.
    This can be called directly from a shelf button.
    """
    return build_fk()

if __name__ == "__main__":
    run()