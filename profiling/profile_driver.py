#!/usr/bin/env python

from __future__ import print_function
import hatchet as ht
from profiler import Profiler
import os
import glob
import json
import yaml
import sys
import platform
from datetime import datetime
# from pyinstrument import Profiler

prf = Profiler()
configs = None

with open("app.yaml", "r") as f:
    configs = yaml.safe_load(f.read())

if __name__ == "__main__":
    if configs['debug'] == True:
        if len(sys.argv) < 2:
            dirname = "../../hatchet/hatchet/tests/data/hpctoolkit-cpi-database"
        else:
            dirname = sys.argv[1]
        prf.start()
        gf = ht.GraphFrame.from_hpctoolkit(dirname)
        prf.end()
        print("DB: {} \n Runtime: {} \n".format(dirname, prf.getRuntime()))

    elif configs['profile_type'] == "batch":

        # create a directory for this run and dump metadata in there
        profile_runs_dir = "{}_profile_runs/".format(datetime.now().strftime("%m-%d-%Y-%H%M"))
        if not os.path.exists(profile_runs_dir):
            os.mkdir(profile_runs_dir)
            with open(profile_runs_dir+"metadata.txt", "w") as f:
                f.write("Description: {}\n".format(configs['run_metadata']['description']))
                uname = platform.uname()
                f.write("System: {}\n".format(uname.system))
                f.write("Node Name: {}\n".format(uname.node))
                f.write("Release: {}\n".format(uname.release))
                f.write("Version: {}\n".format(uname.version))
                f.write("Machine: {}\n".format(uname.machine))
                f.write("Processor: {}\n".format(uname.processor))

        dirname = configs['profile_endpoint']
        numtrials = configs['numtrials']


        visual_dict = {'profile':[], 'runtime':[], 'records':[], 'nodes':[], 'ranks':[], 'threads': []}
        updateVis = configs['vis']['updateVis']

        if updateVis is True:
            vispath = "vis_data_{}_trials_{}.json".format(numtrials, configs['run_output_postfix'])
        else:
            vispath = profile_runs_dir+"temp_vis_store.json"

        if os.path.exists(vispath):
            print("Reading old timing code.")
            with open(vispath, "r") as f:
                visual_dict = json.loads(f.read())

        for filename in os.listdir(dirname):
            print("Profiling", filename)
            for x in range(0, numtrials):
                print(".", end='')
                prf.start()
                gf = ht.GraphFrame.from_hpctoolkit(dirname + filename)
                prf.end()

            print('\n')
            prf.dumpAverageStats('cumulative', profile_runs_dir+'{1}_records_{2}_trials_{0}_{3}_profile.txt'.format(filename, gf.dataframe.shape[0], numtrials, configs['run_output_postfix']), numtrials)
            visual_dict['profile'].append(filename)
            visual_dict['runtime'].append(prf.getAverageRuntime(numtrials))
            visual_dict['records'].append(gf.dataframe.shape[0])

            threads = gf.dataframe.groupby(['thread']).sum()
            visual_dict['threads'].append(threads.shape[0])

            ranks = gf.dataframe.groupby(['rank']).sum()
            visual_dict['ranks'].append(ranks.shape[0])

            nodes = gf.dataframe.groupby(['node']).sum()
            visual_dict['nodes'].append(nodes.shape[0])

            prf.reset()

        # get the last directory from dirname
        with open(vispath, 'w') as f:
            f.write(json.dumps(visual_dict))

    elif configs['profile_type'] == "single":
        dir = configs['profile_endpoint']
        filename = configs['filename']
        numtrials = configs['numtrials']

        print("Profiling", filename)
        for x in range(0, numtrials):
            print(".", end='')
            prf.start()
            gf = ht.GraphFrame.from_hpctoolkit(dir+filename)
            prf.end()

        prf.dumpAverageStats('cumulative', '{1}_records_{2}_trials_{0}_profile.txt'.format(configs['filename'], gf.dataframe.shape[0], numtrials), numtrials)




    # print(gf.dataframe.shape)
    # print("\n")




    # print(gf.tree(threshold=0.0))
