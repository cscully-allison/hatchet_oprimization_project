import hatchet as ht
from util.db import MetadataDB

md_db = MetadataDB()

# Configuration file specific information
name = 'app.py'
descripton = 'This is configuration file for the hatchet profilier.'

# Configurations for the profilier driver
log_to_db = True
run_metadata = {
    'description': 'Doing a 1 trial scaling run on unoptimized graphframe.filter(). Filtering half the graph frame.',
    'keywords': 'filter operation graphframe.filter pre-optimization unoptimized Ian reduce_by_half 1_trial'
}

debug = False
debug_conf = {
        'files': [
        '/g/g16/scullyal/ws/hatchet/hatchet/tests/data/hpctoolkit-cpi-database',
        '/g/g16/scullyal/ws/hatchet/hatchet/tests/data/hpctoolkit-threads-osu-allgather',
        '/usr/workspace/asde/hatchet-datasets/mpi-perf-comparison-datasets/hpctoolkit-database-amg2013-mvapich2-64-0'
        ],
        'selection': 2,
        'output': False
}

# advanced querying
# eliminating redundant files from
# scaling study
redundant_files = [8,20,18,22,4,12,26,30,28]
files = md_db.p_md.loc[(md_db.p_md['setname'] == 'Ian')]
files = files[~files.index.isin(redundant_files)]

run_configuration = {
    'file_selection': files,
    'profile_type': 'batch',
    'numtrials': 5,
    'md_indx': 22
}
