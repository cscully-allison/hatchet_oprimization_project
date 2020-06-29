#!/usr/bin/env python3

import hatchet as ht
from profiler import Profiler
import os
import glob
import json
import yaml
# from pyinstrument import Profiler

prf = Profiler()
configs = None

with open("app.yaml", "r") as f:
    configs = yaml.safe_load(f.read())

if __name__ == "__main__":
    if configs['debug'] == True:
        dirname = "../../hatchet/hatchet/tests/data/hpctoolkit-threads-osu-allgather"
        gf = ht.GraphFrame.from_hpctoolkit(dirname)

    elif configs['profile_type'] == "batch":
        dirname = configs['profile_endpoint']
        numtrials = configs['numtrials']


        visual_dict = {'profile':[],'runtime':[],'records':[]}
        vispath = "vis_data_{}_trials.json".format(numtrials)
        updateVis = True

        if os.path.exists(vispath) and updateVis:
            print("Reading old timing code.")
            with open(vispath, "r") as f:
                visual_dict = json.loads(f.read())

        for filename in os.listdir(dirname):
            print("Profiling", filename)
            for x in range(0, numtrials):
                print(".", end='')
                prf.start()
                gf = ht.GraphFrame.from_hpctoolkit(dirname + filename)
                # gf = ht.GraphFrame.from_hpctoolkit(dirname)
                # prf.stop()
                prf.end()


            # with open("prof_2.html".format(dirname),"w") as f:
            # with open("{}_prof_1.html".format(filename),"w") as f:
                # f.write(prf.output_html())

            # prf = Profiler()
            # prf.dumpSortedStats('cumulative', 'cprofile_2.txt')
            print('\n')
            prf.dumpAverageStats('cumulative', '{1}_records_{2}_trials_{0}_profile.txt'.format(filename, gf.dataframe.shape[0], numtrials), numtrials)
            visual_dict['profile'].append(filename)
            visual_dict['runtime'].append(prf.getAverageRuntime(numtrials))
            visual_dict['records'].append(gf.dataframe.shape[0])
            prf.reset()

        # get the last directory from dirname
        with open(vispath, 'w') as f:
            f.write(json.dumps(visual_dict))

    elif configs['profile_type'] == "single":
        filename = configs['profile_endpoint']
        numtrials = configs['numtrials']

        print("Profiling", filename)
        for x in range(0, numtrials):
            print(".", end='')
            prf.start()
            gf = ht.GraphFrame.from_hpctoolkit(filename)
            prf.end()

        prf.dumpAverageStats('cumulative', '{1}_records_{2}_trials_{0}_profile.txt'.format(configs['filename'], gf.dataframe.shape[0], numtrials), numtrials)
        



    # print(gf.dataframe.shape)
    # print("\n")




    # print(gf.tree(threshold=0.0))
