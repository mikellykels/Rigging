import maya.cmds as cmds

def build_groups():
    """
    Build the base group hierarchy for the rig.

    This function creates a standardized group structure for organizing
    different components of the rig. The hierarchy is as follows:

    ROOT
    |-- CONTROLS
    |-- DO_NOT_TOUCH
        |-- EXPORT_SKELETON
        |-- GEO
        |-- RIG_DEFORMERS
        |-- RIG_SYSTEMS

    If the ROOT group already exists, it uses the existing one.
    For all other groups, it creates them if they don't already exist.

    Returns:
        str: The name of the ROOT group.
    """

    # Define the hierarchy
    hierarchy = {
        'ROOT': ['CONTROLS', 'DO_NOT_TOUCH'],
        'DO_NOT_TOUCH': ['EXPORT_SKELETON', 'GEO', 'RIG_DEFORMERS', 'RIG_SYSTEMS'],
    }

    # Create or get the ROOT group
    if not cmds.objExists('ROOT'):
        root = cmds.group(empty=True, name='ROOT')
    else:
        root = 'ROOT'

    # Create the child groups if they don't exist
    for parent, children in hierarchy.items():
        for child in children:
            full_path = f'{parent}|{child}'
            if not cmds.objExists(full_path):
                if parent == 'ROOT':
                    cmds.group(empty=True, name=child, parent=root)
                else:
                    cmds.group(empty=True, name=child, parent=parent)

    print('Base rig structure created successfully.')
    return root

def run():
    """
    Main function to build the base rig structure.
    This can be called directly from a shelf button.
    """
    return build_groups()

if __name__ == "__main__":
    run()