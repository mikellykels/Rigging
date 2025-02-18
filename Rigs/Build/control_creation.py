import maya.cmds as cmds

def create_fk_controls(control_template, joints):
    """
    Create FK controls for the given joints using a control template.

    This function performs the following steps:
    1. Creates an offset group for each joint.
    2. Duplicates the control template for each joint.
    3. Renames each duplicated control based on the joint name (removing '_FK' and adding '_ctrl').
    4. Creates an offset group for each control, named with '_offset' suffix.
    5. Matches the position and orientation of each offset group to its corresponding joint.
    6. Parents the control to its offset group.
    7. Parents the offset group to the previous control (not offset group) if applicable.
    8. Constrains the joint to its corresponding control using a parent constraint.

    Args:
        control_template (str): The name of the NURBS curve to use as a template for the controls.
        joints (list): A list of joint names to create controls for.

    Returns:
        list: A list of the created control names, or an empty list if an error occurred.
    """
    if not cmds.objExists(control_template):
        cmds.warning(f"Control template '{control_template}' does not exist.")
        return []

    if not joints:
        cmds.warning("No joints provided to create controls for.")
        return []

    created_controls = []

    # Find the FKIK switch control
    switch_ctrl = None
    for obj in cmds.ls():
        if cmds.attributeQuery('FKIK_Switch', node=obj, exists=True):
            switch_ctrl = obj
            break

    # Create a reverse node for FK visibility if switch control exists
    reverse_node = None
    if switch_ctrl:
        reverse_node = cmds.createNode('reverse', name=f"{switch_ctrl}_FKIK_reverse")
        cmds.connectAttr(f"{switch_ctrl}.FKIK_Switch", f"{reverse_node}.inputX")

    for i, joint in enumerate(joints):
        # Create the new control name
        ctrl_name = joint.replace('_FK', '_ctrl') if '_FK' in joint else f"{joint}_ctrl"
        offset_name = joint.replace('_FK', '_offset') if '_FK' in joint else f"{joint}_offset"

        # Duplicate the control template
        new_control = cmds.duplicate(control_template, name=ctrl_name)[0]

        # Set the color override to blue
        ctrl_shape = cmds.listRelatives(new_control, shapes=True)[0]
        cmds.setAttr(f"{ctrl_shape}.overrideEnabled", 1)
        cmds.setAttr(f"{ctrl_shape}.overrideColor", 6)  # 6 is blue in Maya's color index

        # Create offset group
        offset_group = cmds.group(empty=True, name=offset_name)

        # Match offset group's transform to the joint
        cmds.matchTransform(offset_group, joint)

        # Parent control to offset group
        cmds.parent(new_control, offset_group)

        # If it's not the first control, parent the offset group to the previous control
        if i > 0:
            cmds.parent(offset_group, created_controls[-1])

        # Constrain the joint to the control
        cmds.parentConstraint(new_control, joint)

        # Zero out the control's transformations
        cmds.xform(new_control, translation=[0, 0, 0], rotation=[0, 0, 0], scale=[1, 1, 1])

        # Connect visibility to reversed FKIK switch if it exists
        # FK controls should be visible when switch is 0
        if reverse_node:
            cmds.connectAttr(f"{reverse_node}.outputX", f"{offset_group}.visibility")

        created_controls.append(new_control)

    return created_controls

def create_ik_control(control_template, joint, control_name=None, offset_name=None):
    """
    Create an IK control for the given joint using a control template.

    Args:
        control_template (str): The name of the NURBS curve to use as a template.
        joint (str): The joint name to create control for.
        control_name (str): Optional specific name for the control.
        offset_name (str): Optional specific name for the offset group.

    Returns:
        tuple: (control name, offset group name), or (None, None) if creation fails
    """
    if not cmds.objExists(control_template):
        cmds.warning(f"Control template '{control_template}' does not exist.")
        return None, None

    if not joint:
        cmds.warning("No joint provided to create control for.")
        return None, None

    # Use provided names or create default ones
    if not control_name:
        control_name = joint.replace('_IK', '_ik_ctrl') if '_IK' in joint else f"{joint}_ik_ctrl"
    if not offset_name:
        offset_name = joint.replace('_IK', '_ik_offset') if '_IK' in joint else f"{joint}_ik_offset"

    # Duplicate the control template
    control = cmds.duplicate(control_template, name=control_name)[0]

    # Create offset group
    offset_group = cmds.group(empty=True, name=offset_name)

    # Match offset group's transform to the joint
    cmds.matchTransform(offset_group, joint)

    # Parent control to offset group
    cmds.parent(control, offset_group)

    # Zero out the control's transformations
    cmds.setAttr(f"{control}.translate", 0, 0, 0)
    cmds.setAttr(f"{control}.rotate", 0, 0, 0)
    cmds.setAttr(f"{control}.scale", 1, 1, 1)

    return control, offset_group

def run_create_ik_control():
    """
    Main function to create IK control based on user selection.

    Usage:
    1. Select the control curve template first.
    2. Select the target joint.
    3. Run this function.
    """
    selection = cmds.ls(selection=True)

    if len(selection) != 2:
        cmds.error("Please select a control template curve followed by target joint.")
        return None, None

    control_template = selection[0]
    target_joint = selection[1]

    # Check if the control template is actually a NURBS curve
    shape_nodes = cmds.listRelatives(control_template, shapes=True) or []
    if not shape_nodes or cmds.nodeType(shape_nodes[0]) != "nurbsCurve":
        cmds.error("The first selected object must be a NURBS curve to use as a control template.")
        return None, None

    # Check if the second selection is a joint
    if cmds.nodeType(target_joint) != "joint":
        cmds.error("The second selection must be a joint.")
        return None, None

    control, offset_group = create_ik_control(control_template, target_joint)
    if control and offset_group:
        print(f"Created IK control {control} with offset group {offset_group}")
        return control, offset_group
    else:
        cmds.warning("Failed to create IK control. Check the script editor for details.")
        return None, None

def run_create_fk_controls():
    """
    Main function to create FK controls based on user selection.

    Usage:
    1. Select the control curve template first.
    2. Shift-select all the FK joints you want to create controls for.
    3. Run this function.
    """
    selection = cmds.ls(selection=True)

    if len(selection) < 2:
        cmds.error("Please select a control template curve followed by target joints.")
        return

    control_template = selection[0]
    target_joints = selection[1:]

    # Check if the control template is actually a NURBS curve
    shape_nodes = cmds.listRelatives(control_template, shapes=True) or []
    if not shape_nodes or cmds.nodeType(shape_nodes[0]) != "nurbsCurve":
        cmds.error("The first selected object must be a NURBS curve to use as a control template.")
        return

    # Check if the last selected item is a joint
    if cmds.nodeType(target_joints[-1]) != "joint":
        cmds.error(
            "The last selected item must be a joint. Please ensure you select the control template first, followed by joints.")
        return

    created_controls = create_fk_controls(control_template, target_joints)
    if created_controls:
        print(f"Created {len(created_controls)} FK controls with offset groups: {', '.join(created_controls)}")
    else:
        cmds.warning("Failed to create FK controls. Check the script editor for details.")

def run():
    """
    Main function to create FK controls.
    This can be called directly from a shelf button.
    """
    return run_create_fk_controls()

if __name__ == "__main__":
    run()