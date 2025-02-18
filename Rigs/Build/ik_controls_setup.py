import maya.cmds as cmds
from . import control_creation

def setup_ik_controls():
    """
    Setup IK controls after FKIK blend is complete.
    IK joints are already in place, this just adds:
    - IK handle from shoulder to wrist
    - Wrist control
    """
    # Get the selected objects
    selection = cmds.ls(selection=True)

    # Check selection count
    if len(selection) < 5:  # Control curve + 3 IK joints + FKIK switch control
        cmds.warning(
            "Please select: Control curve template, 3 IK joints, and FKIK switch control")
        return None, None

    # Split selection
    ik_control_curve = selection[0]
    ik_joints = selection[1:4]
    switch_ctrl = selection[4]

    # Verify first selection is a curve
    if not cmds.nodeType(cmds.listRelatives(ik_control_curve, shapes=True)[0]) == 'nurbsCurve':
        cmds.warning("First selection must be a NURBS curve to use as a control template")
        return None, None

    # Verify joints
    if not all(cmds.nodeType(joint) == 'joint' for joint in ik_joints):
        cmds.warning("Joints must be selected after control curve")
        return None, None

    # Verify FKIK switch attribute exists
    if not cmds.attributeQuery('FKIK_Switch', node=switch_ctrl, exists=True):
        cmds.warning("FKIK switch control must have FKIK_Switch attribute")
        return None, None

    # Create IK handle
    ik_handle = create_ik_handle(ik_joints[0], ik_joints[-1])

    # Create main IK control at wrist
    control, offset_group = control_creation.create_ik_control(ik_control_curve, ik_joints[-1])

    # Set the color override to blue
    ctrl_shape = cmds.listRelatives(control, shapes=True)[0]
    cmds.setAttr(f"{ctrl_shape}.overrideEnabled", 1)
    cmds.setAttr(f"{ctrl_shape}.overrideColor", 6)  # 6 is blue

    # Parent IK handle under control
    cmds.parent(ik_handle, control)

    # Setup visibility connections for IK system
    # When FKIK_Switch is 1, IK is visible
    # Connect to the offset group to affect entire IK system
    cmds.connectAttr(f"{switch_ctrl}.FKIK_Switch", f"{offset_group}.visibility")

    # Hide IK handle
    cmds.setAttr(f"{ik_handle}.visibility", 0)

    # Connect IK joint visibility to FKIK switch
    for joint in ik_joints:
        cmds.connectAttr(f"{switch_ctrl}.FKIK_Switch", f"{joint}.visibility")

    return ik_handle, control

def create_ik_handle(start_joint, end_joint):
    """
    Create an IK handle between two joints using rotate plane solver.
    """
    base_name = start_joint.replace('_IK', '').replace('_shoulder', '')
    ik_handle_name = f"{base_name}_ikHandle"

    # Get middle joint (elbow)
    children = cmds.listRelatives(start_joint, children=True, type='joint') or []
    if children:
        mid_joint = children[0]  # This should be the elbow
        # Set preferred angle for natural bend
        cmds.setAttr(f"{mid_joint}.preferredAngleY", -90)

    # Create IK handle with specific settings
    ik_handle = cmds.ikHandle(
        name=ik_handle_name,
        startJoint=start_joint,
        endEffector=end_joint,
        solver='ikRPsolver'
    )

    return ik_handle[0]

def run():
    """
    Main function to setup IK controls.
    This can be called directly from a shelf button.
    """
    return setup_ik_controls()

if __name__ == "__main__":
    run()