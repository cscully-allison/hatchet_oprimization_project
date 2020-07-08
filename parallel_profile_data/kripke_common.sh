
nranks=$1

traceprefix="rank"
nnodes=64
appname=kripke
problem_name="kripke"
problem_desc=""
#common_inputdata=" --groups 512 --zones 92,92,92 --quad 512 "
common_inputdata=" --groups 64 --zones 192,144,96 --quad 64 "

source run_${nnodes}_${nranks}_common.sh
tracefilepath="/g/g92/marathe1/traces/kripke_traces/${nnodes}/${nranks}"
inputdata=`echo "${common_inputdata} ${rank_input} --niter 5"`

process_per_sampler=`echo "${nranks_per_socket} * 2" | bc`
cd ${appdir}

dramlim=0
for nestiter in ${nestlist};
do
#        echo "Nesting1=${nestiter}"
        for layoutiter in 0 1; # 0==Blocked, 1==Scattered
        do
            for dsetiter in 8 16 32 64;
            do
                for gsetiter in 1 2 4 8 16 32 64;
                do
                    for methoditer in sweep bj;
                    do
                        for ompiter in ${omplist}; 
                        do
                                appdir=/g/g92/marathe1/benchmarks/kripke_mod/build_golden/
                                curr_trace="${tracefilepath}/n${nestiter}/l${layoutiter}d${dsetiter}g${gsetiter}m${methoditer}t${ompiter}"

                                retval2=`(wc -l ${tracefilepath}/n${nestiter}/l${layoutiter}d${dsetiter}g${gsetiter}m${methoditer}t${ompiter}/output 2> /dev/null) | cut -d " " -f 1`
                                if [ \( "$retval2" == "" \) -o \( "$retval2" == "0" \) -o \( "$retval2" == "1" \) ];
                                then

                                    mkdir -p ${curr_trace}
                                    chmod 766 ${curr_trace} -R
                                    local_input=" --nest ${nestiter} --layout ${layoutiter} --dset ${dsetiter} --gset ${gsetiter} --zset 1,1,1 --pmethod ${methoditer}"

#                                    echo "${local_input} $curr_trace"

                                    (OMP_NUM_THREADS=${ompiter} \
                                     KMP_AFFINITY=compact \
                                     time srun -N ${nnodes} -n ${nranks} \
                                     -m block \
                                     --cpu_bind=rank \
                                     --ntasks-per-socket=${nranks_per_socket} \
                                     --sockets-per-node=${sockets_per_node} \
                                     --msr-safe \
                                     ${appdir}/${appname} ${inputdata} ${local_input} 2>&1) >& ${curr_trace}/output
                                else 
                                    echo "Exists"
                                fi
                        done
                    done
                done
            done
        done
done
