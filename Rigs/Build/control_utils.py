import maya.cmds as cmds

def add_fkik_switch_attribute(control):
    """
    Add the FKIK_Switch attribute to the selected control.

    Args:
        control (str): The name of the control object.

    Returns:
        bool: True if the attribute was added successfully, False otherwise.
    """
    if not cmds.objExists(control):
        cmds.warning(f"Control '{control}' does not exist.")
        return False

    if not cmds.attributeQuery('FKIK_Switch', node=control, exists=True):
        cmds.addAttr(control, longName='FKIK_Switch', attributeType='float', min=0, max=1, defaultValue=0, keyable=True)
        print(f"Added FKIK_Switch attribute to {control}")
        return True
    else:
        print(f"FKIK_Switch attribute already exists on {control}")
        return False

def run():
    """
    Main function to add FKIK_Switch attribute to the selected control.
    This can be called directly from a shelf button.

    Returns:
        bool: True if the attribute was added successfully, False otherwise.
    """
    selected = cmds.ls(selection=True)
    if selected:
        return add_fkik_switch_attribute(selected[0])
    else:
        cmds.warning("Please select a control object.")
        return False

if __name__ == "__main__":
    run()