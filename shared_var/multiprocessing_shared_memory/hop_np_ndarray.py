import numpy as np
from multiprocessing import shared_memory, resource_tracker

d_shape = (10,)
d_type = np.int64
shm_name = 'test_shm_np'

try:
  # In other processes
  # reuse existing shared memory
  ex_shm = shared_memory.SharedMemory(name=shm_name, create=False)
  resource_tracker.unregister(ex_shm._name, 'shared_memory')
  # numpy array on existing memory buffer, a and b read/write the same memory
  b = np.ndarray(shape=d_shape, dtype=d_type, buffer=ex_shm.buf)
  print('len(b): ', len(b))
  print('b[1]: ', b[1])
  b[1] += 1
  print('b: ', b)

  ex_shm.close()  # close after using
except FileNotFoundError:
  print('Error: shared memory {} does not exist'.format(shm_name))
