import numpy as np
from hatchet.util.profiler import Profiler

cdef where(long[:] intarr, int num_ints):
  ndx_store = np.zeros((1000),dtype=np.int64)
  cdef long[:] ndx_store_view = ndx_store
  cdef int n_ndx
  n_ndx = 0

  for i in range(num_ints):
    if intarr[i] == intarr[3]:
      ndx_store_view[n_ndx] = i
      if n_ndx < 1000-1:
        n_ndx += 1

  return ndx_store


def np_test():
    prf = Profiler()
    print("Generating")
    test = np.random.randint(100000, size=5000000)
    print("Generated")

    prf.start()

    # cdef long[:] test_view = test

    out = where(test, test.shape[0])

    print(out)

    prf.end()

    print(prf.getRuntime())
