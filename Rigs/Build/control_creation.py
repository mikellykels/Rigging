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

    for i, joint in enumerate(joints):
        # Create the new control name
        ctrl_name = joint.replace('_FK', '_ctrl') if '_FK' in joint else f"{joint}_ctrl"
        offset_name = joint.replace('_FK', '_offset') if '_FK' in joint else f"{joint}_offset"

        # Duplicate the control template
        new_control = cmds.duplicate(control_template, name=ctrl_name)[0]

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

        created_controls.append(new_control)

    return created_controls

def run_create_fk_controls():
    """
    Main function to create FK controls based on user selection.

    This function:
    1. Gets the currently selected objects in Maya.
    2. Ensures the first selected object is the control template (NURBS curve).
    3. Ensures all other selected objects are joints to create controls for.
    4. Calls create_fk_controls() with these arguments.
    5. Prints the results or any errors.

    Usage:
    1. Select the control curve template first.
    2. Shift-select all the FK joints you want to create controls for.
    3. Run this function.

    This function is designed to be called directly or from a shelf button.
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