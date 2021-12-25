from multiprocessing.managers import SharedMemoryManager
from multiprocessing import shared_memory, resource_tracker

"""
from .resource_tracker import register

create = True
if create:
 register(self._name, "shared_memory")
"""

with SharedMemoryManager() as smm:
  ### sl = smm.ShareableList(range(20))
  shm = shared_memory.SharedMemory(name='test_smm', size=10, create=True)
  ### resource_tracker.unregister(shm._name, 'shared_memory')
  print('shm._name: ', shm._name)
  ### print('sl.shm.name: ', sl.shm.name)
  ### print('sl: ', sl)

  input("Press Enter to continue")
