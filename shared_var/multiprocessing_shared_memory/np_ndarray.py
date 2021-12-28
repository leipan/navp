import numpy as np
from multiprocessing import shared_memory, resource_tracker

shm_name = 'test_shm_np'

### data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
data = range(0, 1000000)
d_shape = (len(data),)
d_type = np.int64
d_size = np.dtype(d_type).itemsize * np.prod(d_shape)

# In main process
# allocate new shared memory
shm = shared_memory.SharedMemory(name=shm_name, create=True, size=d_size)
shm_name = shm.name
# numpy array on shared memory buffer
a = np.ndarray(shape=d_shape, dtype=d_type, buffer=shm.buf)
# copy data into shared memory ndarray once
a[:] = data[:]

print('a[1]: ', a[1])

input("Press Enter to continue")

# In main process
shm.close()  # close after using
shm.unlink()  # free memory
