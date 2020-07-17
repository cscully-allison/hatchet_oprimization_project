import os
from sys import argv
import json
import pandas as pd
import numpy as np
import hatchet as ht
import fnmatch

class DB():
        def __init__(self):
            self.p_md = None
            self.db_name = None
            self.categories = {}

        def read_db(self):
            if not os.path.exists(self.db_name):
                f = open(self.db_name, "w")
                f.write(
                    json.dumps(
                        self.categories
                    )
                )
                f.close()

            self.p_md = pd.read_json(self.db_name)

            for cat in self.categories:
                if cat not in self.p_md:
                    self.p_md[cat] = np.nan

        def rm(self, indexes):
            self.read_db()
            self.p_md = self.p_md.drop(indexes)
            self.p_md.to_json(self.db_name)


class DataDB(DB):
    def __init__(self):
        self.p_md = None
        self.db_name = "/usr/workspace/scullyal/hatchet_optimization_project/db/profile_data_db.json"
        self.categories = {
                            'profile':[],
                            'dir':[],
                            'md_id':[],
                            'runtime':[],
                            'description':[],
                            'keywords':[],
                            'run_id':[],
                            'datetime':[]
                            }
        self.read_db()

    def add(self, row):
        self.read_db()
        print(row)
        self.p_md['datetime'] = self.p_md['datetime'].astype(str)
        self.p_md = self.p_md.append(row, ignore_index=True)
        print(self.p_md)
        self.p_md.to_json(self.db_name)



class MetadataDB(DB):
    def __init__(self):
        self.p_md = None
        self.db_name = "/usr/workspace/scullyal/hatchet_optimization_project/db/metadata_db.json"
        self.setname = "test"
        self.categories = {
                                "filename": [],
                                "filepath": [],
                                "setname": [],
                                "nodes":[],
                                "threads": [],
                                "ranks": [],
                                "callsites": [],
                                "records": [],
                                "num-db-files": [],
                                "size-on-disk": [],
                                "filetype": [],
                                "other": []
                            }
        self.cleanup_db()
        self.read_db()


    def cleanup_db(self):
        # remove broken or inaccessable links
        self.read_db()
        for index, row in self.p_md.iterrows():
            if( not os.path.exists(row['filepath'])):
                self.p_md = self.p_md.drop([index])
        self.p_md.to_json(self.db_name)


    def collect_md_cali(self, filename, gf, fqn, query):
        md = {
            "filename": "",
            "filepath": "",
            "setname": "",
            "callsites": 0,
            "records": 0,
            "filetype": "Caliper",
            "other": query
        }
        total_size = 0
        num_files = 0
        nids = []
        nodes = 0

        # algorithm for finding node-ids
        base = 0
        first = True

        # collect runtime data
        for dir in fqn.split('/'):
            if 'NODES' in dir:
                run_info = dir.split('.')
                md["nodes"] = int(run_info[1])
                md["ranks"] = int(run_info[3])

        callsites = gf.dataframe.groupby(["node"]).sum()

        md["filename"] = filename
        md["filepath"] = os.path.abspath(fqn)
        md["setname"] = self.setname

        md["callsites"] = callsites.shape[0]
        md["records"] = gf.dataframe.shape[0]

        self.p_md = self.p_md.append(md, ignore_index=True)

        return md

    def single_add_cali(self, fqn, query, setname=None, signficant_folders=1):
        self.read_db()

        # get correct filename from last part of fqn
        # conditions for trailing / or no /
        lastOffset = -signficant_folders
        if fqn.split("/")[lastOffset] is not "":
            filename = fqn.split("/")[lastOffset]
        else:
            lastOffset -= 1
            filename = fqn.split("/")[lastOffset]

        if setname == None:
            self.setname = fqn.split("/")[lastOffset - 1]
        else:
            self.setname = setname

        for i in range(lastOffset+1, 0, 1):
            filename += "/" + fqn.split("/")[i]

        if (filename not in self.p_md["filename"].values):
            gf = ht.GraphFrame.from_caliper(fqn, query)
            self.collect_md_cali(filename, gf, fqn, query)
            print(self.p_md)
        else:
            print("Warning: {} already in database.".format(filename))

        self.p_md.to_json(self.db_name)

    def collect_md(self, filename, gf, fqn):
        md = {
            "filename": "",
            "filepath": "",
            "setname": "",
            "nodes": 0,
            "threads": 1,
            "ranks": 0,
            "callsites": 0,
            "records": 0,
            "num-db-files": 0,
            "size-on-disk": 0,
            "filetype": "HPCToolkit"
        }
        total_size = 0
        num_files = 0
        nids = []
        nodes = 0

        # algorithm for finding node-ids
        base = 0
        first = True

        #collect hpctoolkit data
        for f in os.listdir(fqn):
            if fnmatch.fnmatch(f, "*.metric-db"):
                # size in bytes
                if fqn[-1] is not '/':
                    fqn += '/'
                total_size += os.path.getsize(fqn+f)
                num_files += 1

                if first is True:
                    while not f.split('-')[base+1].isnumeric():
                        base += 1
                    first = False


                # push on unique node ids
                nid = f.split("-")[base+3]
                if nid not in nids:
                    nids.append(nid)

        nodes = len(nids)

        # collect hatchet data
        print(gf.dataframe.index.names)
        if "thread" in gf.dataframe.index.names or "thread" in gf.dataframe:
            threads = gf.dataframe.groupby(["thread"]).sum()
        ranks = gf.dataframe.groupby(["rank"]).sum()
        callsites = gf.dataframe.groupby(["node"]).sum()

        md["filename"] = filename
        md["filepath"] = os.path.abspath(fqn)
        md["setname"] = self.setname

        md["num-db-files"] = num_files
        md["size-on-disk"] = total_size
        md["nodes"] = nodes

        if "thread" in gf.dataframe.index.names or "thread" in gf.dataframe:
            md["threads"] = threads.shape[0]
        md["ranks"] = ranks.shape[0]
        md["callsites"] = callsites.shape[0]
        md["records"] = gf.dataframe.shape[0]

        self.p_md = self.p_md.append(md, ignore_index=True)

        return md

    def batch_add(self, dir="./", setname=None):
        self.setname = setname
        self.read_db()

        for file in os.listdir(dir):
            filename = file
            if dir == ".":
                fqn = filename
            else:
                fqn = dir + filename

            if setname == None:
                self.setname = fqn.split("/")[-3]
            else:
                self.setname = setname

            # check if same dataset essentially
            if (filename not in self.p_md["filename"].values):
                print("Attempting to add file: {}".format(file))
                try:
                    print("Loading graphframe")
                    gf = ht.GraphFrame.from_hpctoolkit(fqn)
                    print("Done loading graphframe")
                    self.collect_md(filename, gf, fqn)
                    print(self.p_md)
                except:
                    print("{} is not a valid hpctoolkit db file.".format(filename))
            else:
                print("{} already in database.".format(filename))


            self.p_md.to_json(self.db_name)

    def single_add(self, fqn, setname=None):
        self.read_db()

        # get correct filename from last part of fqn
        # conditions for trailing / or no /
        lastOffset = -1
        if fqn.split("/")[lastOffset] is not "":
            filename = fqn.split("/")[lastOffset]
        else:
            lastOffset -= 1
            filename = fqn.split("/")[lastOffset]

        if setname == None:
            self.setname = fqn.split("/")[lastOffset - 1]
        else:
            self.setname = setname

        if (filename not in self.p_md["filename"].values):
            gf = ht.GraphFrame.from_hpctoolkit(fqn)
            self.collect_md(filename, gf, fqn)
            print(self.p_md)
        else:
            print("Warning: {} already in database.".format(filename))

        self.p_md.to_json(self.db_name)

    def inspect_md(self, fqn):
        filename = ""
        lastOffset = -1
        if fqn.split("/")[lastOffset] is not "":
            filename = fqn.split("/")[lastOffset]
        else:
            lastOffset -= 1
            filename = fqn.split("/")[lastOffset]

        gf = ht.GraphFrame.from_hpctoolkit(fqn)

        md = self.collect_md(filename, gf, fqn)

        for x in md:
            print("{}: {}".format(x, md[x]))


        # print("Filename: {}".format(fqn.split("/")[-2]))
        # print("Filepath: {}".format(os.path.abspath(fqn)))
        # print("Nodes: {}")
        # print("Threads: {}".format(threads.shape[0]))
        # print("Ranks: {}".format(ranks.shape[0]))
        # print("Callsites: {}".format(callsites.shape[0]))
        # print("Records: {}".format(gf.dataframe.shape[0]))
        # print("Superset: {}".format(self.setname))
