#!/bin/bash
#SBATCH -N 4
#SBATCH -t 01:00:00
#SBATCH -p pdebug
#SBATCH --output=job%J.out
#SBATCH --error=job%J.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=scullyalliso1@llnl.gov

#--------#
# Quartz #
#--------#

module load hpctoolkit/2019.08.14

#can't find: hacckernels, laghos, nekbone
APPS_MPICH=( \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/amg2013/amg2013-master-mpich-3.3.2-gcc-4.9.3/bin/amg2013" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/cloverleaf/cloverleaf-1.1-mpich-3.3.2-gcc-4.9.3/bin/clover_leaf" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/ior/ior-3.2.1-mpich-3.3.2-gcc-4.9.3/bin/ior" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/kripke/kripke-1.2.4-mpich-3.3.2-gcc-4.9.3/bin/kripke.exe" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/lammps/lammps-20200505-mpich-3.3.2-gcc-4.9.3/bin/lmp" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/macsio/macsio-1.1-mpich-3.3.2-gcc-4.9.3/macsio" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/minife/minife-2.1.0-mpich-3.3.2-gcc-4.9.3/bin/miniFE.x" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/pennant/pennant-0.9-mpich-3.3.2-gcc-4.9.3/bin/pennant" \
)
SRC_MPICH=( \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/amg2013/amg2013-master-mpich-3.3.2-gcc-4.9.3/share/amg2013/src" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/cloverleaf/cloverleaf-1.1-mpich-3.3.2-gcc-4.9.3/share/cloverleaf/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/ior/ior-3.2.1-mpich-3.3.2-gcc-4.9.3/share/ior/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/kripke/kripke-1.2.4-mpich-3.3.2-gcc-4.9.3/share/kripke/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/lammps/lammps-20200505-mpich-3.3.2-gcc-4.9.3/share/lammps/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/macsio/macsio-1.1-mpich-3.3.2-gcc-4.9.3/share/macsio/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/minife/minife-2.1.0-mpich-3.3.2-gcc-4.9.3/share/minife/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/pennant/pennant-0.9-mpich-3.3.2-gcc-4.9.3/share/pennant/src/" \
)

APPS_MVAPICH=( \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/amg2013/amg2013-master-mvapich2-2.3.3-gcc-4.9.3/bin/amg2013" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/cloverleaf/cloverleaf-1.1-mvapich2-2.3.3-gcc-4.9.3/bin/clover_leaf" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/ior/ior-3.2.1-mvapich2-2.3.3-gcc-4.9.3/bin/ior" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/kripke/kripke-1.2.4-mvapich2-2.3.3-gcc-4.9.3/bin/kripke.exe" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/lammps/lammps-20200505-mvapich2-2.3.3-gcc-4.9.3/bin/lmp" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/macsio/macsio-1.1-mvapich2-2.3.3-gcc-4.9.3/macsio" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/minife/minife-2.1.0-mvapich2-2.3.3-gcc-4.9.3/bin/miniFE.x" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/pennant/pennant-0.9-mvapich2-2.3.3-gcc-4.9.3/bin/pennant" \
)
SRC_MVAPICH=( \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/amg2013/amg2013-master-mvapich2-2.3.3-gcc-4.9.3/share/amg2013/src" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/cloverleaf/cloverleaf-1.1-mvapich2-2.3.3-gcc-4.9.3/share/cloverleaf/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/ior/ior-3.2.1-mvapich2-2.3.3-gcc-4.9.3/share/ior/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/kripke/kripke-1.2.4-mvapich2-2.3.3-gcc-4.9.3/share/kripke/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/lammps/lammps-20200505-mvapich2-2.3.3-gcc-4.9.3/share/lammps/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/macsio/macsio-1.1-mvapich2-2.3.3-gcc-4.9.3/share/macsio/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/minife/minife-2.1.0-mvapich2-2.3.3-gcc-4.9.3/share/minife/src/" \
    "/usr/workspace/wsb/asde/spack/var/spack/environments/benchmarking-quartz/views/full/pennant/pennant-0.9-mvapich2-2.3.3-gcc-4.9.3/share/pennant/src/" \
)

# array is 0 indexed, change based on which application you want to run
idx=3

# switch between MPICH and MVAPICH arrays
APP=${APPS_MVAPICH[${idx}]}
SRC=${SRC_MVAPICH[${idx}]}

NAME=$(echo $APP | rev | cut -d "/" -f 1 | rev)

# single thread per rank in metric-db file
export OMP_NUM_THREADS=1
export HPCRUN_IGNORE_THREAD=1

srun -n 64 hpcrun ${APP} --procs 4,4,4

hpcstruct $APP

srun -N 1 hpcprof-mpi -S ${NAME}.hpcstruct \
                      -I ${SRC} \
                      --metric-db yes \
                      hpctoolkit-${NAME}-measurements-*

#
