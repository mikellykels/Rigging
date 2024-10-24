import maya.cmds as cmds
from . import control_utils

def match_joints(joints):
    """
    Match FK, IK, and export joints based on their names.

    Args:
        joints (list): List of all joint names.

    Returns:
        tuple: Lists of export, FK, and IK joints.
    """
    export_joints = []
    fk_joints = []
    ik_joints = []

    for joint in joints:
        if joint.endswith('_FK'):
            fk_joints.append(joint)
        elif joint.endswith('_IK'):
            ik_joints.append(joint)
        else:
            export_joints.append(joint)

    # Sort joints to ensure they're in the same order
    export_joints.sort()
    fk_joints.sort()
    ik_joints.sort()

    return export_joints, fk_joints, ik_joints

def create_fkik_blend_joints(export_joints, fk_joints, ik_joints, control):
    """
    Create blend joints that switch between FK and IK joints.

    Args:
        export_joints (list): List of original (export skeleton) joint names.
        fk_joints (list): List of FK joint names.
        ik_joints (list): List of IK joint names.
        control (str): The name of the control object with the FKIK_Switch attribute.

    Returns:
        list: List of created blend nodes.
    """
    if len(export_joints) != len(fk_joints) or len(export_joints) != len(ik_joints):
        cmds.warning("The number of export, FK, and IK joints must be the same.")
        return None

    # Add FKIK_Switch attribute to the control
    control_utils.add_fkik_switch_attribute(control)

    # Determine the side prefix (l_ or r_) based on the first joint
    side_prefix = 'l_' if export_joints[0].startswith('l_') else 'r_'

    # Create a single reverse node for all joints
    reverse_node = cmds.createNode('reverse', name=f"{side_prefix}FKIK_reverse")
    cmds.connectAttr(f"{control}.FKIK_Switch", f"{reverse_node}.inputX")

    blend_nodes = []

    for export_joint, fk_joint, ik_joint in zip(export_joints, fk_joints, ik_joints):
        # Create parent constraint
        constraint = cmds.parentConstraint(fk_joint, ik_joint, export_joint)[0]

        # Get the weight attributes of the constraint
        weights = cmds.parentConstraint(constraint, q=True, weightAliasList=True)

        # Connect the FKIK_Switch attribute to the constraint weights
        # FKIK_Switch: 0 = FK, 1 = IK
        cmds.connectAttr(f"{control}.FKIK_Switch", f"{constraint}.{weights[1]}")  # IK weight
        cmds.connectAttr(f"{reverse_node}.outputX", f"{constraint}.{weights[0]}")  # FK weight

        blend_nodes.append(constraint)

    return blend_nodes

def build_fkik_blend():
    """
    Main function to build the FK/IK blend system.
    Selects all joints and the control, then creates the blend system.

    Returns:
        list: List of created blend nodes, or None if selection is incorrect.
    """
    # Get the selected objects
    selected = cmds.ls(selection=True)

    if len(selected) < 4:  # At least one set of joints (3) plus the control (1)
        cmds.warning("Please select all FK, IK, and export joints, and then the control object.")
        return None

    # The last selected item is the control
    control = selected[-1]
    joints = selected[:-1]

    # Match the joints
    export_joints, fk_joints, ik_joints = match_joints(joints)

    if not (export_joints and fk_joints and ik_joints):
        cmds.warning("Could not find matching sets of FK, IK, and export joints.")
        return None

    # Create the blend system
    blend_nodes = create_fkik_blend_joints(export_joints, fk_joints, ik_joints, control)

    return blend_nodes

def run():
    """
    Main function to build the FK IK blend system.
    This can be called directly from a shelf button.
    """
    return build_fkik_blend()

if __name__ == "__main__":
    run()