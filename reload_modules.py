import importlib

def reload_modules():
    from .Rigs.Build import (
        base_rig,
        joint_utils,
        fk_build,
        control_creation,
        ik_build,
        ik_controls_setup,
        control_utils,
        fkik_blend_build
    )

    importlib.reload(base_rig)
    importlib.reload(joint_utils)
    importlib.reload(fk_build)
    importlib.reload(control_creation)
    importlib.reload(ik_build)
    importlib.reload(ik_controls_setup)
    importlib.reload(control_utils)
    importlib.reload(fkik_blend_build)

    print("Modules reloaded successfully")

if __name__ == "__main__":
    reload_modules()