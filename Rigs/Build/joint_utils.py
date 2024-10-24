import maya.cmds as cmds

def get_joint_info():
    """
    Retrieve hierarchy information for selected joints in the Maya scene.

    This function performs the following steps:
    1. Selects all joints in the current Maya selection.
    2. For each selected joint, it gathers information about its parent and children.
    3. Stores this information in a dictionary structure.

    Returns:
        dict: A dictionary where each key is a joint name, and each value is another
              dictionary containing:
              - 'parent': The name of the parent joint (or None if no parent)
              - 'children': A list of child joint names (or an empty list if no children)

    If no joints are selected, the function will display a warning and return None.

    Example returned structure:
    {
        'joint1': {
            'parent': None,
            'children': ['joint2', 'joint3']
        },
        'joint2': {
            'parent': 'joint1',
            'children': []
        },
        'joint3': {
            'parent': 'joint1',
            'children': ['joint4']
        },
        'joint4': {
            'parent': 'joint3',
            'children': []
        }
    }
    """

    # Get selected joints
    selected_joints = cmds.ls(selection=True, type='joint')

    if not selected_joints:
        cmds.warning('No joints selected. Please select some joints')
        return

    # Store joint hierarchy information
    joint_info = {}

    for joint in selected_joints:
        parent = cmds.listRelatives(joint, parent=True, type='joint')
        children = cmds.listRelatives(joint, children=True, type='joint')

        joint_info[joint] = {
            'parent': parent[0] if parent else None,
            'children': children if children else [],
        }

def duplicate_and_rename_joints(joints, suffix):
    """
    Duplicate the selected joints and rename them with the given suffix.
    Then, recreate the hierarchy of the duplicated joints.

    Args:
        joints (list): List of original joint names.
        suffix (str): Suffix to add to the duplicated joints (e.g., '_FK', '_IK').

    Returns:
        list: List of duplicated and renamed joint names.
    """
    new_joints = []

    # Iterate through each selected joint
    for joint in joints:
        # Duplicate the joint without its children
        duplicated = cmds.duplicate(joint, parentOnly=True)

        if duplicated:
            # Remove '_jnt' from the joint name if present
            base_name = joint.replace('_jnt', '')

            # Create the new name with the given suffix
            new_name = f"{base_name}{suffix}"

            # Rename the duplicated joint
            renamed = cmds.rename(duplicated[0], new_name)

            # Add the renamed joint to our list
            new_joints.append(renamed)

    # Recreate the hierarchy for the duplicated joints
    if len(new_joints) > 1:
        # Start from the second joint (index 1)
        for i in range(1, len(new_joints)):
            # Parent each joint to the previous one in the list
            cmds.parent(new_joints[i], new_joints[i - 1])

    return new_joints

def run():
    """
    Main function to get joint information.
    This replaces the run.py functionality.
    """
    return get_joint_info()

if __name__ == "__main__":
    # Execute get_joint_info
    joint_info = get_joint_info()

    # If joints are selected, execute duplicate_and_rename_joints for both FK and IK
    if joint_info:
        selected_joints = cmds.ls(selection=True, type='joint')
        duplicate_and_rename_joints(selected_joints, '_FK')
        duplicate_and_rename_joints(selected_joints, '_IK')