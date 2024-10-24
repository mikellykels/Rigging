import maya.cmds as cmds
from . import control_creation

def setup_ik_controls():
    """
    Setup IK controls after FKIK blend is complete.

    Required selection order:
    1. Three IK joints in order (e.g., shoulder_IK, elbow_IK, wrist_IK)
    2. The corresponding three export joints (e.g., shoulder, elbow, wrist)
    3. IK control curve
    4. Pole vector control curve
    5. The control with FKIK switch attribute

    Returns:
        tuple: (str IK handle name, str IK control name, str pole vector control name)
    """
    # Get the selected objects
    selection = cmds.ls(selection=True)

    # Check selection count
    if len(selection) != 9:  # 3 IK joints + 3 export joints + 2 control curves + switch control
        cmds.warning(
            "Please select: 3 IK joints, 3 export joints, IK control curve, pole vector curve, and FKIK switch control")
        return None, None, None

    # Split selection
    ik_joints = selection[0:3]
    export_joints = selection[3:6]
    ik_control_curve = selection[6]
    pv_curve = selection[7]
    switch_ctrl = selection[8]

    # Verify joints
    if not all(cmds.nodeType(joint) == 'joint' for joint in ik_joints + export_joints):
        cmds.warning("First six selections must be joints")
        return None, None, None

    # Verify curves
    if not all(cmds.nodeType(cmds.listRelatives(curve, shapes=True)[0]) == 'nurbsCurve'
               for curve in [ik_control_curve, pv_curve]):
        cmds.warning("Last two selections must be NURBS curves")
        return None, None, None

    # Create IK handle
    ik_handle = create_ik_handle(ik_joints[0], ik_joints[-1])

    # Create main IK control
    control, offset_group = control_creation.create_ik_control(ik_control_curve, ik_joints[-1])

    # Setup IK specific connections
    cmds.orientConstraint(control, ik_joints[-1], maintainOffset=True)
    cmds.parent(ik_handle, control)

    # Create pole vector control
    pv_control = setup_pole_vector(pv_curve, ik_joints, ik_handle, control)

    # Connect visibility to FKIK switch
    if cmds.attributeQuery('FKIK_Switch', node=switch_ctrl, exists=True):
        # Get the line group (it will follow our naming convention)
        line_grp = f"{ik_joints[1]}_pv_line_grp"

        # Add line group to our visibility list
        visible_items = [control, pv_control, ik_handle, line_grp] + ik_joints

        for item in visible_items:
            if cmds.objExists(item):  # Make sure the item exists
                parent = cmds.listRelatives(item, parent=True)
                vis_target = parent[0] if parent else item

                existing_conn = cmds.listConnections(f"{vis_target}.visibility", source=True, destination=False)
                if not existing_conn:
                    cmds.connectAttr(f"{switch_ctrl}.FKIK_Switch", f"{vis_target}.visibility")

    return ik_handle, control, pv_control

def create_ik_handle(start_joint, end_joint):
    """
    Create an IK handle between two joints using rotate plane solver.
    """
    base_name = start_joint.replace('_IK', '')
    ik_handle_name = f"{base_name}_ikHandle"

    ik_handle = cmds.ikHandle(
        name=ik_handle_name,
        startJoint=start_joint,
        endEffector=end_joint,
        solver='ikRPsolver'
    )

    return ik_handle[0]

def setup_pole_vector(pv_curve, ik_joints, ik_handle, ik_control):
    """
    Setup pole vector control and create a reference line.
    """
    mid_joint = ik_joints[1]  # IK elbow joint

    # Rename pole vector control
    base_name = mid_joint.replace('_IK', '')
    pv_control_name = f"{base_name}_pv_ctrl"
    pv_control = cmds.rename(pv_curve, pv_control_name)

    # Create offset group for pole vector control
    pv_offset = cmds.group(empty=True, name=f"{pv_control_name}_offset")

    # Get joint positions to calculate chain length
    start_pos = cmds.xform(ik_joints[0], query=True, worldSpace=True, translation=True)
    mid_pos = cmds.xform(mid_joint, query=True, worldSpace=True, translation=True)
    end_pos = cmds.xform(ik_joints[2], query=True, worldSpace=True, translation=True)

    # Calculate chain length
    def get_distance(pos1, pos2):
        return ((pos2[0] - pos1[0]) ** 2 +
                (pos2[1] - pos1[1]) ** 2 +
                (pos2[2] - pos2[2]) ** 2) ** 0.5

    chain_length = get_distance(start_pos, mid_pos) + get_distance(mid_pos, end_pos)
    offset_dist = chain_length * 0.8

    # Position at elbow and move forward
    cmds.setAttr(f"{pv_offset}.translate",
                 mid_pos[0],  # X - Same as elbow
                 mid_pos[1],  # Y - Same as elbow
                 mid_pos[2] - offset_dist)  # Z - Move forward

    # Parent control under offset
    cmds.parent(pv_control, pv_offset)

    # Reset control transforms
    cmds.setAttr(f"{pv_control}.translate", 0, 0, 0)
    cmds.setAttr(f"{pv_control}.rotate", 0, 0, 0)
    cmds.setAttr(f"{pv_control}.scale", 1, 1, 1)

    # Create pole vector constraint
    cmds.poleVectorConstraint(pv_control, ik_handle)

    # Parent offset under IK control
    cmds.parent(pv_offset, ik_control)

    # Create reference line
    create_pole_vector_line(mid_joint, pv_control)

    return pv_control

def create_pole_vector_line(mid_joint, pv_control):
    """
    Create a reference line between the middle joint and pole vector control.
    """
    # Create locators at both ends
    loc1 = cmds.spaceLocator(name=f"{mid_joint}_pv_loc1")[0]
    loc2 = cmds.spaceLocator(name=f"{mid_joint}_pv_loc2")[0]

    # Make locators small and hidden
    for loc in [loc1, loc2]:
        cmds.setAttr(f"{loc}.localScale", 0.1, 0.1, 0.1)
        cmds.setAttr(f"{loc}.visibility", 0)

    # Parent constrain locators
    cmds.parentConstraint(mid_joint, loc1)
    cmds.parentConstraint(pv_control, loc2)

    # Create curve between locators
    line = cmds.curve(name=f"{mid_joint}_pv_line", degree=1, point=[(0, 0, 0), (1, 0, 0)])

    # Create cluster at each CV
    cv1 = f"{line}.cv[0]"
    cv2 = f"{line}.cv[1]"
    clust1 = cmds.cluster(cv1, name=f"{mid_joint}_pv_clust1")[1]
    clust2 = cmds.cluster(cv2, name=f"{mid_joint}_pv_clust2")[1]

    # Hide clusters
    cmds.setAttr(f"{clust1}.visibility", 0)
    cmds.setAttr(f"{clust2}.visibility", 0)

    # Constrain clusters to locators
    cmds.parentConstraint(loc1, clust1)
    cmds.parentConstraint(loc2, clust2)

    # Group everything
    line_grp = cmds.group([line, loc1, loc2, clust1, clust2],
                          name=f"{mid_joint}_pv_line_grp")

    # Style the line
    curve_shape = cmds.listRelatives(line, shapes=True)[0]
    cmds.setAttr(f"{curve_shape}.lineWidth", 1)
    cmds.setAttr(f"{curve_shape}.overrideEnabled", 1)
    cmds.setAttr(f"{curve_shape}.overrideColor", 18)  # light blue

    return line_grp

def run():
    """
    Main function to setup IK controls.
    This can be called directly from a shelf button.
    """
    return setup_ik_controls()

if __name__ == "__main__":
    run()