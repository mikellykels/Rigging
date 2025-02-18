import maya.cmds as cmds
from . import run

class RiggingUI:
    """
    Main UI class for the rigging tools.

    This UI provides a centralized interface for all rigging operations:
    - BuildBase: Creates the standard group hierarchy for the rig
    (More functionality to be added...)
    """

    def __init__(self):
        self.window_name = "rigging_tools_ui"
        self.window_title = "Rigging Tools"

        # Close any existing window
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        # Create new window with resize enabled
        self.window = cmds.window(
            self.window_name,
            title=self.window_title,
            width=300,
            resizeToFitChildren=True  # Add this line
        )

        # Create main layout
        self.main_layout = cmds.columnLayout(
            adjustableColumn=True,
            columnAlign="center"
        )

        # Add description text
        cmds.text(
            label="Rigging Tools",
            font="boldLabelFont",
            height=30
        )

        cmds.separator(height=10, style='none')

        # Build Base section
        cmds.frameLayout(
            label="Base Setup",
            collapsable=True,
            collapse=False,
            marginWidth=5,
            marginHeight=5,
            collapseCommand=lambda: self.resize_window(),
            expandCommand=lambda: self.resize_window()
        )

        # Add description for Build Base
        cmds.text(
            label="Creates the standard group hierarchy for the rig:",
            align="left"
        )
        cmds.text(
            label="ROOT",
            align="left",
            font="plainLabelFont"
        )
        cmds.text(
            label="  ├─ CONTROLS",
            align="left",
            font="plainLabelFont"
        )
        cmds.text(
            label="  └─ DO_NOT_TOUCH",
            align="left",
            font="plainLabelFont"
        )
        cmds.text(
            label="      ├─ EXPORT_SKELETON",
            align="left",
            font="plainLabelFont"
        )
        cmds.text(
            label="      ├─ GEO",
            align="left",
            font="plainLabelFont"
        )
        cmds.text(
            label="      ├─ RIG_DEFORMERS",
            align="left",
            font="plainLabelFont"
        )
        cmds.text(
            label="      └─ RIG_SYSTEMS",
            align="left",
            font="plainLabelFont"
        )

        cmds.separator(height=10, style='none')

        # Add Build Base button
        cmds.button(
            label="Build Base",
            command=self.build_base,
            height=35
        )

        cmds.setParent('..')  # Exit frame layout

        # Build FK section
        cmds.frameLayout(
            label="FK Setup",
            collapsable=True,
            collapse=False,
            marginWidth=5,
            marginHeight=5,
            collapseCommand=lambda: self.resize_window(),
            expandCommand=lambda: self.resize_window()
        )

        # Add description for Build FK
        cmds.text(
            label="Select the joints you want to create FK controls for",
            align="left"
        )
        cmds.text(
            label="(e.g. l_shoulder_jnt, l_elbow_jnt, l_wrist_jnt)",
            align="left",
            font="obliqueLabelFont"
        )

        cmds.separator(height=10, style='none')

        # Add Build FK button
        cmds.button(
            label="Build FK",
            command=self.build_fk,
            height=35
        )

        cmds.setParent('..')  # Exit frame layout

        # Build IK section
        cmds.frameLayout(
            label="IK Setup",
            collapsable=True,
            collapse=False,
            marginWidth=5,
            marginHeight=5,
            collapseCommand=lambda: self.resize_window(),
            expandCommand=lambda: self.resize_window()
        )

        # Add description for Build IK
        cmds.text(
            label="Select the joints you want to create IK controls for",
            align="left"
        )
        cmds.text(
            label="(e.g. l_shoulder_jnt, l_elbow_jnt, l_wrist_jnt)",
            align="left",
            font="obliqueLabelFont"
        )

        cmds.separator(height=10, style='none')

        # Add Build IK button
        cmds.button(
            label="Build IK",
            command=self.build_ik,
            height=35
        )

        cmds.setParent('..')  # Exit frame layout

        # Build FKIK Blend section
        cmds.frameLayout(
            label="FKIK Blend Setup",
            collapsable=True,
            collapse=False,
            marginWidth=5,
            marginHeight=5,
            collapseCommand=lambda: self.resize_window(),
            expandCommand=lambda: self.resize_window()
        )

        # Add description for FKIK Blend
        cmds.text(
            label="Select in this order:",
            align="left"
        )
        cmds.text(
            label="1. All FK joints (e.g. l_shoulder_FK, l_elbow_FK, l_wrist_FK)",
            align="left",
            font="obliqueLabelFont"
        )
        cmds.text(
            label="2. All IK joints (e.g. l_shoulder_IK, l_elbow_IK, l_wrist_IK)",
            align="left",
            font="obliqueLabelFont"
        )
        cmds.text(
            label="3. All base joints (e.g. l_shoulder_jnt, l_elbow_jnt, l_wrist_jnt)",
            align="left",
            font="obliqueLabelFont"
        )
        cmds.text(
            label="4. The FKIK switch control",
            align="left",
            font="obliqueLabelFont"
        )

        cmds.separator(height=10, style='none')

        # Add Build FKIK Blend button
        cmds.button(
            label="Build FKIK Blend",
            command=self.build_fkik_blend,
            height=35
        )

        cmds.setParent('..')  # Exit frame layout

        # Build FK Controls section
        cmds.frameLayout(
            label="FK Controls Setup",
            collapsable=True,
            collapse=False,
            marginWidth=5,
            marginHeight=5,
            collapseCommand=lambda: self.resize_window(),
            expandCommand=lambda: self.resize_window()
        )

        # Add description for FK Controls
        cmds.text(
            label="Select in this order:",
            align="left"
        )
        cmds.text(
            label="1. Control curve (at origin) to use as template",
            align="left",
            font="obliqueLabelFont"
        )
        cmds.text(
            label="2. FK joints (e.g. l_shoulder_FK, l_elbow_FK, l_wrist_FK)",
            align="left",
            font="obliqueLabelFont"
        )

        cmds.separator(height=10, style='none')

        # Add Build FK Controls button
        cmds.button(
            label="Build FK Controls",
            command=self.build_fk_controls,
            height=35
        )

        cmds.setParent('..')  # Exit frame layout

        # Build IK Controls section
        cmds.frameLayout(
            label="IK Controls Setup",
            collapsable=True,
            collapse=False,
            marginWidth=5,
            marginHeight=5,
            collapseCommand=lambda: self.resize_window(),
            expandCommand=lambda: self.resize_window()
        )

        # Add description for IK Controls
        cmds.text(
            label="Select in this order:",
            align="left"
        )
        cmds.text(
            label="1. Control curve template",
            align="left",
            font="obliqueLabelFont"
        )
        cmds.text(
            label="2. IK joints (e.g. l_shoulder_IK, l_elbow_IK, l_wrist_IK)",
            align="left",
            font="obliqueLabelFont"
        )
        cmds.text(
            label="3. FKIK switch control",
            align="left",
            font="obliqueLabelFont"
        )

        cmds.separator(height=10, style='none')

        # Add Build IK Controls button
        cmds.button(
            label="Build IK Controls",
            command=self.build_ik_controls,
            height=35
        )

        cmds.setParent('..')  # Exit frame layout

        # Show window
        cmds.showWindow(self.window)

        cmds.window(self.window, edit=True, h=10)  # Start small
        cmds.showWindow(self.window)

    def resize_window(self):
        """Resize window to fit content when sections are collapsed/expanded"""
        cmds.window(self.window, edit=True, h=10)  # Reset height small
        cmds.window(self.window, edit=True, resizeToFitChildren=True)  # Resize to fit

    def build_base(self, *args):
        """
        Execute the build_base operation and provide feedback.
        """
        try:
            root = run.run_build_base()
            if root:
                cmds.confirmDialog(
                    title="Success",
                    message="Base rig structure created successfully!",
                    button=["OK"],
                    defaultButton="OK"
                )
        except Exception as e:
            cmds.confirmDialog(
                title="Error",
                message=f"Failed to create base rig structure: {str(e)}",
                button=["OK"],
                defaultButton="OK"
            )

    def build_fk(self, *args):
        """
        Execute the build_fk operation and provide feedback.
        Includes warning handling for proper user feedback.
        """
        # Get selected joints
        selected = cmds.ls(selection=True, type='joint')

        if not selected:
            cmds.warning("Please select joints to build FK system")
            cmds.confirmDialog(
                title="Selection Required",
                message="Please select the joints you want to create FK controls for.\nExample: select l_arm_01, l_arm_02, l_arm_03",
                button=["OK"],
                defaultButton="OK"
            )
            return

        try:
            # Attempt to build FK system
            fk_joints = run.run_build_fk()

            if fk_joints:
                message = "FK joints created successfully:\n"
                for joint in fk_joints:
                    message += f"\n- {joint}"

                cmds.confirmDialog(
                    title="Success",
                    message=message,
                    button=["OK"],
                    defaultButton="OK"
                )
            else:
                cmds.confirmDialog(
                    title="Warning",
                    message="No FK joints were created. Check script editor for details.",
                    button=["OK"],
                    defaultButton="OK"
                )
        except Exception as e:
            cmds.confirmDialog(
                title="Error",
                message=f"Failed to create FK system: {str(e)}",
                button=["OK"],
                defaultButton="OK"
            )

    def build_ik(self, *args):
        """
        Execute the build_ik operation and provide feedback.
        Includes warning handling for proper user feedback.
        """
        # Get selected joints
        selected = cmds.ls(selection=True, type='joint')

        if not selected:
            cmds.warning("Please select joints to build IK system")
            cmds.confirmDialog(
                title="Selection Required",
                message="Please select the joints you want to create IK controls for.\nExample: select l_shoulder_jnt, l_elbow_jnt, l_wrist_jnt",
                button=["OK"],
                defaultButton="OK"
            )
            return

        try:
            # Attempt to build IK system
            ik_joints = run.run_build_ik()

            if ik_joints:
                message = "IK joints created successfully:\n"
                for joint in ik_joints:
                    message += f"\n- {joint}"

                cmds.confirmDialog(
                    title="Success",
                    message=message,
                    button=["OK"],
                    defaultButton="OK"
                )
            else:
                cmds.confirmDialog(
                    title="Warning",
                    message="No IK joints were created. Check script editor for details.",
                    button=["OK"],
                    defaultButton="OK"
                )
        except Exception as e:
            cmds.confirmDialog(
                title="Error",
                message=f"Failed to create IK system: {str(e)}",
                button=["OK"],
                defaultButton="OK"
            )

    def build_fkik_blend(self, *args):
        """
        Execute the build_fkik_blend operation and provide feedback.
        Includes warning handling for proper user feedback.
        """
        # Get all selected objects
        selected = cmds.ls(selection=True)

        if len(selected) < 10:  # At least 9 joints (3 sets of 3) plus the control
            cmds.warning("Incorrect selection. Please select all required joints and the FKIK switch control.")
            cmds.confirmDialog(
                title="Selection Required",
                message="Please select in this order:\n\n" +
                        "1. FK joints (e.g. l_shoulder_FK, l_elbow_FK, l_wrist_FK)\n" +
                        "2. IK joints (e.g. l_shoulder_IK, l_elbow_IK, l_wrist_IK)\n" +
                        "3. Base joints (e.g. l_shoulder_jnt, l_elbow_jnt, l_wrist_jnt)\n" +
                        "4. FKIK switch control",
                button=["OK"],
                defaultButton="OK"
            )
            return

        try:
            # Attempt to build FKIK blend system
            blend_nodes = run.run_build_fkik_blend()

            if blend_nodes:
                message = "FKIK blend system created successfully!\n"
                message += "\nCreated blend nodes:"
                for node in blend_nodes:
                    message += f"\n- {node}"

                cmds.confirmDialog(
                    title="Success",
                    message=message,
                    button=["OK"],
                    defaultButton="OK"
                )
            else:
                cmds.confirmDialog(
                    title="Warning",
                    message="FKIK blend system was not created. Check script editor for details.",
                    button=["OK"],
                    defaultButton="OK"
                )
        except Exception as e:
            cmds.confirmDialog(
                title="Error",
                message=f"Failed to create FKIK blend system: {str(e)}",
                button=["OK"],
                defaultButton="OK"
            )

    def build_fk_controls(self, *args):
        """
        Execute the build_fk_controls operation and provide feedback.
        Includes warning handling for proper user feedback.
        """
        # Get selected objects
        selection = cmds.ls(selection=True)

        if len(selection) < 2:  # Need at least control template and one joint
            cmds.warning("Please select control template and FK joints")
            cmds.confirmDialog(
                title="Selection Required",
                message="Please select in this order:\n\n" +
                        "1. Control curve template\n" +
                        "2. FK joints (e.g. l_shoulder_FK, l_elbow_FK, l_wrist_FK)",
                button=["OK"],
                defaultButton="OK"
            )
            return

        # Check if first selection is a NURBS curve
        shape_nodes = cmds.listRelatives(selection[0], shapes=True) or []
        if not shape_nodes or cmds.nodeType(shape_nodes[0]) != "nurbsCurve":
            cmds.confirmDialog(
                title="Invalid Selection",
                message="The first selected object must be a NURBS curve to use as a control template.",
                button=["OK"],
                defaultButton="OK"
            )
            return

        try:
            # Attempt to create FK controls
            run.run_create_fk_controls()
            cmds.confirmDialog(
                title="Success",
                message="FK controls created successfully!",
                button=["OK"],
                defaultButton="OK"
            )
        except Exception as e:
            cmds.confirmDialog(
                title="Error",
                message=f"Failed to create FK controls: {str(e)}",
                button=["OK"],
                defaultButton="OK"
            )

    def build_ik_controls(self, *args):
        # Get selected objects
        selection = cmds.ls(selection=True)

        if len(selection) < 5:  # Control curve + 3 IK joints + switch control
            cmds.warning("Please select all required objects in the correct order")
            cmds.confirmDialog(
                title="Selection Required",
                message="Please select in this order:\n\n" +
                        "1. Control curve template\n" +
                        "2. Three IK joints (e.g. l_shoulder_IK, l_elbow_IK, l_wrist_IK)\n" +
                        "3. FKIK switch control",
                button=["OK"],
                defaultButton="OK"
            )
            return

        # Check if first selection is a NURBS curve
        ik_curve = selection[0]
        shape_nodes = cmds.listRelatives(ik_curve, shapes=True) or []
        if not shape_nodes or cmds.nodeType(shape_nodes[0]) != "nurbsCurve":
            cmds.confirmDialog(
                title="Invalid Selection",
                message="The first selected object must be a NURBS curve to use as a control template.",
                button=["OK"],
                defaultButton="OK"
            )
            return

        try:
            # Attempt to setup IK controls
            ik_handle, ik_control = run.run_setup_ik_controls()
            cmds.confirmDialog(
                title="Success",
                message="IK controls created successfully!",
                button=["OK"],
                defaultButton="OK"
            )
        except Exception as e:
            cmds.confirmDialog(
                title="Error",
                message=f"Failed to create IK controls: {str(e)}",
                button=["OK"],
                defaultButton="OK"
            )

def show_ui():
    """
    Create and show the rigging UI.
    This can be called from Maya's script editor or added to a shelf button.
    """
    ui = RiggingUI()
    return ui

if __name__ == "__main__":
    show_ui()