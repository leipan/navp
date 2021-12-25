from multiprocessing.managers import SharedMemoryManager

with SharedMemoryManager() as smm:
  sl = smm.ShareableList(range(20))
  print('sl.shm.name: ', sl.shm.name)
  print('sl: ', sl)

  input("Press Enter to continue")
