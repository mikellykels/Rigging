from . import base_rig
from . import joint_utils
from . import fk_build
from . import ik_build
from . import fkik_blend_build
from . import control_creation
from . import ik_controls_setup

def run_build_base():
    return base_rig.build_groups()

def run_get_joint_info():
    return joint_utils.get_joint_info()

def run_build_fk():
    return fk_build.build_fk()

def run_build_ik():
    return ik_build.build_ik()

def run_build_fkik_blend():
    return fkik_blend_build.build_fkik_blend()

def run_create_fk_controls():
    return control_creation.run_create_fk_controls()

def run_setup_ik_controls():
    return ik_controls_setup.run()

if __name__ == "__main__":
    run_build_base()
    run_get_joint_info()
    run_build_fk()
    run_build_ik()
    run_build_fkik_blend()
    run_create_fk_controls()
    run_setup_ik_controls()
