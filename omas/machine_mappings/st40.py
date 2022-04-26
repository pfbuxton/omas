import os
import numpy as np
from inspect import unwrap

from numpy.lib.function_base import iterable
from omas import *
from omas.omas_utils import printd, unumpy
from omas.machine_mappings._common import *

# Tokamak Energy database
from st40_phys_viewer import Get_data

__all__ = []
__regression_arguments__ = {'__all__': __all__}


@machine_mapping_function(__regression_arguments__, pulse=133221)
def equilibrium__tokamak_energy(ods, pulse, code_run):
    """
    Docstring
    """
    printd('Accessing equilibrium data using the ST40 Physics Viewer', topic='machine')

    # By including !r in st40.json python ensures that "__repr__()" is used.
    # The consequence of this is that "EFIT#RUN01" is returned including the quotation marks!
    # So we need to remove the quotation marks
    code_run = code_run.replace('"', '')
    [code_name, run_name] = code_run.split("#")

    # Connect to Tokamak Energy database
    equilibrium_results = Get_data(pulse, code_run)

    # Code name and code settings
    ods['equilibrium.code.name'] = code_name

    # Time
    ods['equilibrium.time'] = equilibrium_results.get('TIME')

    for iTime in range(len(equilibrium_results.get('TIME'))):

        ## "GLOBAL" variables
        ods['equilibrium.time_slice'][iTime]['time'] = equilibrium_results.get('TIME')[iTime]
        ods['equilibrium.time_slice'][iTime]['global_quantities.ip'] = equilibrium_results.get('GLOBAL.IP')[iTime]
        ods['equilibrium.time_slice'][iTime]['global_quantities.li_3'] = equilibrium_results.get('GLOBAL.LI3')[iTime]
        ods['equilibrium.time_slice'][iTime]['global_quantities.q_axis'] = equilibrium_results.get('GLOBAL.Q0')[iTime]
        ods['equilibrium.time_slice'][iTime]['global_quantities.volume'] = equilibrium_results.get('GLOBAL.VPLASMA')[iTime]
        ods['equilibrium.time_slice'][iTime]['global_quantities.energy_mhd'] = equilibrium_results.get('GLOBAL.WMHD')[iTime]

        ## "PSI2D" variables
        # Grid
        RGRID = equilibrium_results.get('PSI2D.FREE.RGRID')
        ZGRID = equilibrium_results.get('PSI2D.FREE.ZGRID')
        [RMesh, ZMesh] = np.meshgrid(RGRID, ZGRID)
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].r'] = RMesh
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].z'] = ZMesh
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].grid.dim1'] = equilibrium_results.get('PSI2D.FREE.RGRID')
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].grid.dim2'] = equilibrium_results.get('PSI2D.FREE.ZGRID')

        # Values
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].psi'] = equilibrium_results.get('PSI2D.FREE.PSI')[iTime, :, :]
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].b_field_r'] = equilibrium_results.get('PSI2D.FREE.BR')[iTime, :, :]
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].b_field_z'] = equilibrium_results.get('PSI2D.FREE.BZ')[iTime, :, :]
        ods['equilibrium.time_slice'][iTime]['profiles_2d[0].b_field_tor'] = equilibrium_results.get('PSI2D.FREE.BPHI')[iTime, :, :]


# ================================
if __name__ == '__main__':
    test_machine_mapping_functions(['thomson_scattering_hardware'], globals(), locals())
