import hatchet as ht
from util.db import MetadataDB

md_db = MetadataDB()

# Configuration file specific information
name = 'app.py'
descripton = 'This is configuration file for the hatchet profilier.'

# Configurations for the profilier driver
run_metadata = {
    'description': 'Testing new configuration file.',
    'keywords': 'test config delete'
}

debug = False
debug_conf = {
        'files': [
        '/g/g16/scullyal/ws/hatchet/hatchet/tests/data/hpctoolkit-cpi-database',
        '/g/g16/scullyal/ws/hatchet/hatchet/tests/data/hpctoolkit-threads-osu-allgather',
        '/usr/workspace/asde/hatchet-datasets/mpi-perf-comparison-datasets/hpctoolkit-database-amg2013-mvapich2-64-0'
        ],
        'selection': 0
}


run_configuration = {
    'file_selection': md_db.p_md.loc[md_db.p_md['setname'] == 'SC19'],
    'profile_type': 'batch',
    'numtrials': 5,
    'md_indx': 18
}
