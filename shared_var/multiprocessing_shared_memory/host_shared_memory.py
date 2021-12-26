from multiprocessing.managers import SharedMemoryManager
from multiprocessing import shared_memory, resource_tracker

### with SharedMemoryManager() as smm:
if True:
  shm = shared_memory.SharedMemory(name='test_smm', size=10, create=True)
  print('shm._name: ', shm._name)

  input("Press Enter to continue")
  shm.unlink()  # free memory
