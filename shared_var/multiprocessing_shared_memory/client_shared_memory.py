from multiprocessing import shared_memory, resource_tracker

name1 = 'test_smm'
try:
  shm = shared_memory.SharedMemory(name='test_smm', size=10, create=False)
  resource_tracker.unregister(shm._name, 'shared_memory')
  ### print('shm: ', shm)
  print('shm.buf: ', shm.buf)
  print('len(shm.buf): ', len(shm.buf))
  print('shm.buf[2]: ', shm.buf[2])
  shm.buf[2] += 1

  for item in shm.buf:
    print(item)

  shm.close()
except FileNotFoundError:
  print('Error: shared memory {} does not exist'.format(name1))
