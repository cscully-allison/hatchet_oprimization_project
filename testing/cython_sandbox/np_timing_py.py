import numpy as np
from hatchet.util.profiler import Profiler

def np_test():
    prf = Profiler()
    print("Generating")
    test = np.random.randint(5000000,1)
    print("Generated")

    print("Where")
    prf.start()
    out1 = np.where(test == test[0])
    prf.end()
    print("Where End")

    print(prf.getRuntime())

    prf.reset()

    print("Loop Start")
    out2 = []
    prf.start()

    for x, i in enumerate(test):
        if x == test[0]:
            out.append(i)

    prf.end()
    print("Loop End")

    print(prf.getRuntime())
